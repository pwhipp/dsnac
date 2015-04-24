from django.contrib import admin
from mediabooks.models import Video, Audio


class VideoAdmin(admin.ModelAdmin):

    def vimeo_link(self):
        vimeo_link = '<a href="http://vimeo.com/%s" target="_blank">http://vimeo.com/%s</a>' % (self.link, self.link)
        return vimeo_link
    vimeo_link.allow_tags = True
    list_display = ['title', 'is_active', vimeo_link]


class AudioAdmin(admin.ModelAdmin):

    def mp3(self):
        mp3 = '<a href="http://sikhnationalarchives.com/media/%s" target="_blank">%s</a>' % (self.mp3, self.mp3)
        return mp3
    mp3.allow_tags = True
    list_display = ['title', mp3]
admin.site.register(Video, VideoAdmin)
admin.site.register(Audio, AudioAdmin)


