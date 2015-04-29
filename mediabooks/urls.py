from __future__ import unicode_literals

from django.conf.urls import patterns, url, include

from mediabooks.views import video, audio, all_videos, all_audios

urlpatterns = patterns(
    '',
    url("^/video/(?P<video_id>\d+)/$", video, name="video_detail"),
    url("^/audio/(?P<audio_id>\d+)/$", audio, name="audio_detail"),
    url("^/videos/$", all_videos, name="all_videos"),
    url("^/audios/$", all_audios, name="all_audios"),
)
