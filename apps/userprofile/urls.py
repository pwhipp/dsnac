from django.conf.urls import patterns, url, include

from .views import dashboard

urlpatterns = patterns(
    '',
    # url(r'^$', DonateView.as_view(), name='donate_extended'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
)
