from django.views.generic import TemplateView

import bookrepo.models as bm

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['recent_scans'] = bm.Book.objects.filter(scanned=True).order_by('-updated')[:10]
        context['slides'] = bm.MainSlider.objects.all()
        return context