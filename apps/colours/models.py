from django.db import models
from colorfield.fields import ColorField


THEMES_CHOICES = (
    ('default', 'Default'),
    ('orange', 'Orange'),
    ('green', 'Green'),
)


class Theme(models.Model):
    active = models.CharField(choices=THEMES_CHOICES, default='default', max_length=255)

    def __unicode__(self):
        return '%s' % self.active


class CustomTheme(models.Model):
    header = ColorField(default='#7a1315')
    body = ColorField(default='#1e2633')
    links = ColorField(default='#ffffff')

    def __unicode__(self):
        return '%s' % self.colour
