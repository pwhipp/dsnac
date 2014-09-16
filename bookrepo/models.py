import os
from django.db import models

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
    ebook = models.BooleanField(default=False)

    def cover_thumbnail_url(self):
        """
        return url for cover thumbnail (not available image url if none)
        :return: url path string
        """
        thumbnail_path = thumbnail_jpg_path(self.identifier)
        if os.path.exists(thumbnail_path):
            return thumbnail_jpg_url(self.identifier)
        else:
            return settings.BOOKS_NO_COVER_IMAGE

# Override inherited verbose content name
Book._meta.get_field('content').help_text = 'Brief description of the books content for searching and web display'


def thumbnail_jpg_path(book_identifier):
    return os.path.join(settings.BOOKS_ROOT,
                        book_identifier,
                        book_identifier+'_cover_thumbnail.jpg')


def thumbnail_jpg_url(book_identifier):
    return settings.BOOKS_URL + book_identifier + '/' + book_identifier + '_cover_thumbnail.jpg'
