from django.db import models

from mezzanine.core.models import RichText, Displayable


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
    title = models.CharField(
        max_length=256, null=True,
        help_text='Full title of book, including subtitle (if any)')
    creator = models.ForeignKey(
        Creator, null=True,
        help_text='The creator of the book, usually the author or authors but may be the editor or a committee.')
    contributor = models.ForeignKey(
        Contributor, null=True,
        help_text='The organisation or individual who contributed the book to the library')
    reference = models.CharField(
        max_length=16, null=True,
        help_text='Library reference number')
    published = models.CharField(
        max_lenth=32,
        help_text='Date of publication (text for now)')
    pages = models.IntegerField(
        default=0,
        help_text="Number of scanned or actual pages (scanned pages takes precedence)")
    scanned = models.BooleanField(default=False)
    ebook = models.BooleanField(default=False)