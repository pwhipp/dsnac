from django.views.generic import TemplateView
from django.core import serializers

from bookrepo.models import Book


class BookReaderView(TemplateView):
    template_name = 'bookreader/reader.html'

    def get_context_data(self, **kwargs):
        context = super(BookReaderView, self).get_context_data(**kwargs)
        book_identifier = self.kwargs['book_identifier']
        page_num = self.kwargs['page_num']
        context['start_page'] = page_num
        context['book'] = Book.objects.get(identifier=book_identifier)
        context['book_json'] = serializers.serialize('json', [context['book']])[1:-2]
        return context