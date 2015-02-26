from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

import bookrepo.views as bv

urlpatterns = patterns(
    '',
    url("^/bookpage/(?P<pk>\d+)/$", bv.BookPageView.as_view(), name="bookpage_detail"),
    url("^/(?P<book_identifier>.+)/(?P<page_number>\d+)/$", bv.page, name="bookrepo_page"),
    url("^/(?P<book_identifier>.+)/thumbnail/$", bv.thumbnail, name="bookrepo_thumbnail"),
    url("^/(?P<book_identifier>.+)/detail/$", bv.BookDetailView.as_view(), name="bookrepo_detail"),
    url("^/$", bv.BookListView.as_view(), name="bookrepo_list"),

    url("^/subjects/$", bv.BookSubjectListView.as_view(), name="bookrepo_subject_list"),
    url("^/(?P<subject_identifier>.+)/subject/$", bv.subject_books, name="bookrepo_subject_detail"),

    url("^/report/$", bv.report_problem, name="bookrepo_report"),

    (r'^/search/', include('haystack.urls')))
