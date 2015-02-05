from __future__ import unicode_literals

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from mezzanine.core.views import direct_to_template
from mezzanine.conf import settings

import bookreader.urls
import bookrepo.urls

from theme.views import HomeView


admin.autodiscover()

urlpatterns = i18n_patterns("", ("^admin/", include(admin.site.urls)))

# Serve static media during development so things look right
if settings.DEBUG:
    urlpatterns += patterns(
        '',
        (r'^{0}/(?P<path>.*)$'.format(settings.MEDIA_URL.strip('/')),
         'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))

urlpatterns += patterns(
    '',
    url("^$", HomeView.as_view(), name="home"),
    ("^bookreader", include(bookreader.urls)),
    ("^bookrepo", include(bookrepo.urls)),
    ("^", include("mezzanine.urls")))+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler404 = "mezzanine.core.views.page_not_found"
handler500 = "mezzanine.core.views.server_error"
