import subprocess
import sys, zipfile, os, os.path

from django.db import models
from django.core.urlresolvers import reverse
from PIL import Image
from pytesseract import image_to_string


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


def content_file_name(instance, filename):
    return '/'.join(['books/', instance.identifier, filename])


class Book(RichText, Displayable):
    """
    A particular edition of a book that is held in the library.
    """
    TYPE_CHOICES = (
        ('Book', 'Book'),
        ('Magazine', 'Magazine'),
        ('Document', 'Document'),
    )
    identifier = models.CharField(
        max_length=255, unique=True,
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
        max_length=255, null=True,
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
    ebook_file = models.FileField(upload_to=content_file_name, null=True, blank=True)
    ebook = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='cover/', default=None, blank=True, null=True)
    book_type = models.CharField(max_length=255, choices=TYPE_CHOICES, blank=True, null=True, default=None,
                                 verbose_name='Material Type')
    is_panjabi = models.BooleanField(default=False, help_text='Select it if book is on Punjabi')

    search_fields = ('title', 'creator__name', 'content')

    def save(self, *args, **kwargs):
        try:
            fullpath, jp2_folder, jpg_folder = self.prepare_book_folders()

            if zipfile.is_zipfile(self.ebook_file.file):
                self.handle_zip_file(fullpath, jp2_folder, jpg_folder)
                # self.remove_file(fullpath, 'zip')

            super(Book, self).save(*args, **kwargs)
        except Exception as e:
            print(e)
            super(Book, self).save(*args, **kwargs)

    def handle_zip_file(self, fullpath, jp2_folder, jpg_folder):
        zfobj = zipfile.ZipFile(self.ebook_file)

        jpg_folder_is_empty = True
        path, dirs, files = os.walk(jpg_folder).next()
        if files:
            jpg_folder_is_empty = False

        jp2_folder_is_empty = True
        path, dirs, files = os.walk(jp2_folder).next()
        if files:
            jp2_folder_is_empty = False

        for name in zfobj.namelist():
            if name.endswith('/'):
                try:
                    os.mkdir(os.path.join(fullpath, name))
                except:
                    pass

            if name.endswith('jp2'):
                if not name.startswith('__MACOSX'):
                    if jp2_folder_is_empty:
                        jp2file = open(os.path.join(jp2_folder, name), 'w+')
                        jp2file.write(zfobj.read(name))
                        jp2file.close()

            elif name.endswith('jpg'):
                if not name.startswith('__MACOSX'):
                    if jpg_folder_is_empty:
                        jpg_file = open(os.path.join(jpg_folder, name), 'w+')
                        jpg_file.write(zfobj.read(name))
                        jpg_file.close()

    @staticmethod
    def remove_file(path, file_type):
        for name in os.listdir(path):
            if name.endswith(file_type):
                os.remove(os.path.join(path, name))

    def get_absolute_url(self):
        return reverse("bookrepo_detail", args=(self.identifier,))

    @property
    def thumbnail_path(self):
        return os.path.join(settings.BOOKS_ROOT,
                            self.identifier,
                            self.identifier + '_cover_thumbnail.jpg')

    def prepare_book_folders(self):
        fullpath = os.path.join('%s/books/%s/') % (settings.MEDIA_ROOT, self.identifier)
        if not os.path.exists(fullpath):
            os.makedirs(fullpath)

        jp2_folder = os.path.join(fullpath, 'jp2')
        if not os.path.exists(jp2_folder):
            os.makedirs(jp2_folder)

        jpg_path = os.path.join(fullpath, 'jpgs')
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)

        return fullpath, jp2_folder, jpg_path

    @property
    def thumbnail_url(self):
        """
        return url for cover thumbnail (not available image url if none)
        :return: url path string

        updated: returning None instead. If scanned thumbnail is not available
        making custom css cover
        """
        pathname = self.thumbnail_path
        if os.path.exists(pathname):
            return settings.BOOKS_URL + self.identifier + '/' + self.identifier + '_cover_thumbnail.jpg'
        else:
            # return settings.BOOKS_NO_COVER_IMAGE
            return None


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
        return os.path.join(settings.BOOKS_ROOT, self.book.identifier, 'jpgs', self.basename + '.jpg')

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
        return os.path.join(settings.BOOKS_ROOT, self.book.identifier, 'jp2', self.basename + '.jp2')

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
        # image = Image.open(self.jp2_pathname)
        image = Image.open(self.jpg_pathname)
        try:
            self.text = image_to_string(image)
        finally:
            image.close()

    def get_absolute_url(self):
        return reverse("bookpage_detail", args=(self.id,))

    def get_in_book_url(self):
        return reverse("bookreader", args=(self.book.identifier, self.num))

    def __unicode__(self):
        return '%s - page %s' % (self.book, self.num)

    def update_punjabi_text_from_image(self):
        image = Image.open(self.jpg_pathname)
        try:
            self.text = image_to_string(image, lang='pan')
        finally:
            image.close()


class MainSlider(models.Model):
    title = models.CharField(max_length=100, verbose_name='Slide name')
    image = models.FileField(upload_to='slider/')
    annotation = models.TextField(verbose_name='annotation', blank=True, null=True, default=None)

    class Meta:
        verbose_name = 'Slider'
        verbose_name_plural = 'slides'

    def __unicode__(self):
        return self.title


class BookUploadLog(models.Model):
    book = models.ForeignKey(Book)
    scanned = models.BooleanField(default=False)
    to_del = models.BooleanField(default=False)
    modified = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return str(self.book)
