from django.conf.urls import patterns, url, include

from .views import dashboard, ChangeCardView

urlpatterns = patterns(
    '',
    # url(r'^$', DonateView.as_view(), name='donate_extended'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^card/$', ChangeCardView.as_view(), name='add_card'),
)
