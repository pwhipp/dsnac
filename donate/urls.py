from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from .views import donate_index, DonateView, donate_paypal

urlpatterns = patterns(
    '',
    url(r'^$', donate_index, name='donate_index'),
    url(r'^extended/$', DonateView.as_view(), name='donate_extended'),
    url(r'^paypal/$', donate_paypal, name='donate_paypal'),
    url(r'^paypal/ipn/', include('paypal.standard.ipn.urls')),
)
