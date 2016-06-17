from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    default_card = models.CharField(max_length=255, blank=True, null=True)
    stripe_id = models.CharField(max_length=255, blank=True, null=True)
    card_last = models.CharField(max_length=255, blank=True, null=True)
    card_expiry = models.CharField(blank=True, null=True, max_length=255)
    payment_active = models.BooleanField(default=False)
    subscribe = models.BooleanField(default=False)

    def __unicode__(self):
        return u'%s' % self.user
