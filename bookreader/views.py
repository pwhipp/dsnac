from django.views.generic import TemplateView


class BookReaderView(TemplateView):
    template_name = 'bookreader/reader.html'

    def get_context_data(self, **kwargs):
        context = super(BookReaderView, self).get_context_data(**kwargs)
        context['book_identifier'] = self.kwargs['book_identifier']
        return context