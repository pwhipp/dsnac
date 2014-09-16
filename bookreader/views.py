from django.views.generic import TemplateView

from bookrepo.models import Book


class BookReaderView(TemplateView):
    template_name = 'bookreader/reader.html'

    def get_context_data(self, **kwargs):
        context = super(BookReaderView, self).get_context_data(**kwargs)
        book_identifier = self.kwargs['book_identifier']
        context['book'] = Book.objects.get(identifier=book_identifier)
        return context