from django.views.generic import TemplateView

from bookrepo.import_books import get_book_meta_data


class BookReaderView(TemplateView):
    template_name = 'bookreader/reader.html'

    def get_context_data(self, **kwargs):
        context = super(BookReaderView, self).get_context_data(**kwargs)
        book_identifier = self.kwargs['book_identifier']
        context['book_identifier'] = book_identifier
        context['book_num_leafs'] = get_book_meta_data(book_identifier=book_identifier)['num_leafs']
        return context