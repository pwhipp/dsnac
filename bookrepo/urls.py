from __future__ import unicode_literals

from django.conf.urls import patterns, url

import bookrepo.views as bv

urlpatterns = patterns(
    '',
    url("^/(?P<book_identifier>.+)/(?P<page_number>\d+)/$", bv.page, name="bookrepo_page"))
