import os

from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

import bookrepo.models as bm


class BookListView(TemplateView):
    template_name = 'bookrepo/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books'] = paginate(self.get_books(), self.request.GET.get("page", 1), 20, settings.MAX_PAGING_LINKS)
        return context

    @staticmethod
    def get_books():
        return bm.Book.objects.all()


class BookDetailView(DetailView):
    model = bm.Book

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, identifier=self.kwargs['book_identifier'])


def thumbnail(request, book_identifier):
    try:
        book = get_object_or_404(bm.Book, identifier=book_identifier)
        return serve_jpg(book.thumbnail_path)
    except IOError:
        raise Http404


def page(request, book_identifier, page_number):
    """
    Return the jpg image corresponding to the specified page
    :param request: Request object
    :param book_identifier: The folder name being used for the book
    :param page_number: integer; 0 < page_number < 9999
    :return:
    """
    try:
        book = get_object_or_404(bm.Book, identifier=book_identifier)
        book_page = get_object_or_404(bm.BookPage, book=book, num=page_number)
        return serve_jpg(book_page.jpg_pathname)
    except IOError:
        raise Http404


def serve_jpg(pathname):
    """
    Return the jpg image in a response
    """
    mime_type = 'image/jpg'
    if os.path.exists(pathname):
        with open(pathname, 'rb') as f:
            response = HttpResponse(f.read(), mimetype=mime_type)
            response['Content-Disposition'] = 'inline;filename={0}'.format(os.path.basename(pathname))
            return response
    else:
        raise Http404