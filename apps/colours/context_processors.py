from .models import Theme


def colour_theme_processor(request):
    try:
        main = Theme.objects.get(id=1)
    except Theme.DoesNotExist:
        main = Theme.objects.create(id=1)
    return {'theme': main.active}

