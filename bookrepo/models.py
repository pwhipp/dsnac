import os
import subprocess

from PIL import Image
from pytesseract import image_to_string

from django.db import models
from django.core.urlresolvers import reverse

from mezzanine.core.models import RichText, Displayable
from mezzanine.conf import settings


class UniqueNamed(models.Model):
    name = models.CharField(max_length=512, unique=True)

    class Meta:
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return u"{0}".format(self.name)


class Creator(UniqueNamed):
    """
    The creator of a book. Usually the Author or Authors. We do not break down authors atm.
    """
    pass


class Contributor(UniqueNamed):
    """
    The contributor of a book.
    """
    pass


class Subject(UniqueNamed):
    """
    The subject of the book
    """
    pass


class Book(RichText, Displayable):
    """
    A particular edition of a book that is held in the library.
    """
    identifier = models.CharField(
        max_length=32, unique=True,
        help_text='Unique identifier for this book edition - used as folder name for book related scan and OCR files')
    creator = models.ForeignKey(
        Creator, null=True,
        help_text='The creator of the book, usually the author or authors but may be the editor or a committee.')
    contributor = models.ForeignKey(
        Contributor, null=True,
        help_text='The organisation or individual who contributed the book to the library')
    subject = models.ForeignKey(
        Subject, null=True,
        help_text='The subject categorization used in the library')
    reference = models.CharField(
        max_length=16, null=True,
        help_text='Library reference number')
    published = models.CharField(
        max_length=32,
        help_text='Date of publication (text for now)')
    num_pages = models.IntegerField(
        default=0,
        help_text="Number of scanned or actual pages (scanned pages takes precedence)")
    num_copies = models.IntegerField(
        default=1,
        help_text="Number of physical copies held by the library")
    scanned = models.BooleanField(default=False)
    scanned_start_page = models.IntegerField(default=0)
    ebook = models.BooleanField(default=False)
    search_fields = ('title', 'creator__name', 'content')

    def get_absolute_url(self):
        return reverse("bookrepo_detail", args=(self.identifier,))

    @property
    def thumbnail_path(self):
        return os.path.join(settings.BOOKS_ROOT,
                            self.identifier,
                            self.identifier + '_cover_thumbnail.jpg')

    @property
    def thumbnail_url(self):
        """
        return url for cover thumbnail (not available image url if none)
        :return: url path string
        """
        pathname = self.thumbnail_path
        if os.path.exists(pathname):
            return settings.BOOKS_URL + self.identifier + '/' + self.identifier + '_cover_thumbnail.jpg'
        else:
            return settings.BOOKS_NO_COVER_IMAGE

# Override inherited verbose content name
Book._meta.get_field('content').help_text = 'Brief description of the books content for searching and web display'


class BookPage(models.Model):
    book = models.ForeignKey(Book)
    num = models.IntegerField(verbose_name='Page number')
    text = models.TextField()

    @property
    def basename(self):
        return '{book_identifier}_{page_number:>04}'.format(
            book_identifier=self.book.identifier,
            page_number=self.num)

    @property
    def _jpg_pathname(self):
        return os.path.join(settings.BOOKS_ROOT,
                            self.book.identifier,
                            'jpgs',
                            self.basename + '.jpg')

    @property
    def jpg_pathname(self):
        """
        Return the pathname if it exists, create and return it otherwise
        """
        pathname = self._jpg_pathname
        if not os.path.exists(pathname):  # create it from the jp2
            jp2_pathname = self.jp2_pathname
            if not subprocess.call(['convert', jp2_pathname, '-resize', '800>', pathname]) == 0:
                raise IOError('{0} conversion failed'.format(jp2_pathname))
        return pathname

    @property
    def _jp2_pathname(self):
        return os.path.join(settings.BOOKS_ROOT,
                            self.book.identifier,
                            '{0}_jp2'.format(self.book.identifier),
                            self.basename + '.jp2')

    @property
    def jp2_pathname(self):
        pathname = self._jp2_pathname
        if not os.path.exists(pathname):
            raise IOError('{0} not found'.format(pathname))
        return pathname

    def update_text_from_image(self):
        """
        Update text attribute using ocr
        :return:
        """
        image = Image.open(self.jpg_pathname)
        try:
            self.text = image_to_string(image)
        finally:
            image.close()

    def get_absolute_url(self):
        return reverse("bookpage_detail", args=(self.id,))

    def get_in_book_url(self):
        return reverse("bookreader", args=(self.book.identifier, self.num))