from django.db import models


class Video(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    link = models.CharField(max_length=255, help_text='for example: https://vimeo.com/47160217')
    description = models.TextField(default=None, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.link:
            self.link = str(self.link).split('/')[-1]
        super(Video, self).save(*args, **kwargs)

    def __unicode__(self):
        return '%s' % self.title


class Audio(models.Model):
    title = models.CharField(max_length=255)
    mp3 = models.FileField(upload_to='audio')
    description = models.TextField(default=None, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.title