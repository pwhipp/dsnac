from __future__ import unicode_literals

from django.conf.urls import patterns, url
from django.views.generic import TemplateView

urlpatterns = patterns(
    '',
    url("^/demo/$", TemplateView.as_view(template_name='bookreader/demo.html'), name="bookreader_demo"))
