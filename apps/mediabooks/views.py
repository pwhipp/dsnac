from django.shortcuts import render
from apps.mediabooks.models import Video, Audio


def video(request, video_id):
    video = Video.objects.get(id=video_id)
    data = {'video': video}
    return render(request, 'video_detail.html', data)


def audio(request, audio_id):
    audio = Audio.objects.get(id=audio_id)
    data = {'audio': audio}
    return render(request, 'audio_detail.html', data)


def all_videos(request):
    videos = Video.objects.filter(is_active=True)
    data = {'videos': videos}
    return render(request, 'video_list.html', data)


def all_audios(request):
    audios = Audio.objects.all()
    data = {'audios': audios}
    return render(request, 'audio_list.html', data)