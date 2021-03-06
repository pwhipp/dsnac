from django.views.generic import TemplateView

import apps.bookrepo.models as bm


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['recent_scans'] = bm.Book.objects.filter(scanned=True).order_by('-updated')[:10]
        context['ebooks'] = bm.Book.objects.filter(ebook=True).order_by('-updated')[:10]
        context['magazines'] = bm.Book.objects.filter(book_type='Magazine')[:10]
        context['slides'] = bm.MainSlider.objects.all()
        return context