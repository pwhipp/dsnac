from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from .views import donate_index

urlpatterns = patterns(
    '',
    url(r'', donate_index, name='donate_index'),
)
