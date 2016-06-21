from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

import apps.bookreader.views as bv

urlpatterns = patterns(
    '',
    url("^/(?P<book_identifier>.+)/(?P<page_num>\d+)/$", login_required(bv.BookReaderView.as_view()), name="bookreader"),
    url("^/demo/$", TemplateView.as_view(template_name='bookreader/demo.html'), name="bookreader_demo"),

    url("^/reading/$", login_required(bv.UsersBooks.as_view()), name='bookreading'),
    url("^/history/$", login_required(bv.UsersHistory.as_view()), name='bookhistory'),
    url("^/(?P<book_identifier>.+)/favorite/$", bv.favorite_book, name="bookfavorite"),
    url("^/favorite/$", login_required(bv.UsersFavorite.as_view()), name="bookfavorite_page"),
    url("^/shelf/$", bv.bookshelf, name="bookshelf"),
    url("^/shelf/add/$", bv.add_book_bookshelf, name="add_book_bookshelf"),
    url("^/myshelves/$", bv.my_shelves, name="mybookshelf"),
    url("^/report/$", bv.report_problem, name="bookrepo_report"),
    url("^/add_book/$", bv.add_book, name="add_book"),

    url("^/type/(?P<book_type>.+)$", bv.books_by_type, name="books_by_type"),

    url("^/(?P<book_identifier>.+)/review/$", login_required(bv.ReviewView.as_view()), name="review"),
)


