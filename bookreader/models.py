from django.db import models
from mezzanine.accounts.views import User
from bookrepo.models import Book


class CommonUsersBooks(models.Model):
    user = models.ForeignKey(User)
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