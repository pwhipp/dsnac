from django.db import models
from django.conf import settings
from apps.bookrepo.models import Book


class CommonUsersBooks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book_identifier = models.ForeignKey(Book)
    added = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

    def __unicode__(self):
        return self.book_identifier


class BookReading(CommonUsersBooks):
    """
    Books that user ever read
    """
    pass


class BookHistory(CommonUsersBooks):
    """
    Visited books
    """
    pass


class FavoriteBook(CommonUsersBooks):
    """
    User's favorite books
    """
    pass


class BookShelf(models.Model):
    name = models.CharField(max_length=255, verbose_name='name', default='Default')
    added = models.DateField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)

    def __unicode__(self):
        return self.name


class UsersShelves(models.Model):
    shelf = models.ForeignKey(BookShelf)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    book = models.ForeignKey(Book)
    added = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.shelf


class Report(models.Model):
    book = models.ForeignKey(Book)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    added = models.DateField(auto_now_add=True)
    fixed = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.user)


class Reviews(CommonUsersBooks):
    rating = models.IntegerField()
    review = models.TextField(default=0)
    headline = models.CharField(max_length=255, default=0)

    def __unicode__(self):
        return str(self.book_identifier)
