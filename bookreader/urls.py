from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

import bookreader.views as bv

urlpatterns = patterns(
    '',
    url("^/(?P<book_identifier>.+)/(?P<page_num>\d+)/$", login_required(bv.BookReaderView.as_view()), name="bookreader"),
    url("^/demo/$", TemplateView.as_view(template_name='bookreader/demo.html'), name="bookreader_demo"))
