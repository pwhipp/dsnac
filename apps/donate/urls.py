from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from .views import DonateView, donate_paypal, donation, CustomerDonateView

urlpatterns = patterns(
    '',
    url(r'^$', DonateView.as_view(), name='donate_extended'),
    url(r'^(?P<donation_id>\d+)/$', donation, name='donation'),
    url(r'^paypal/$', donate_paypal, name='donate_paypal'),
    url(r'^customer/$', CustomerDonateView.as_view(), name='donate_customer'),
    url(r'^paypal/ipn/', include('paypal.standard.ipn.urls')),
)
