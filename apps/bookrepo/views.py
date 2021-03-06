import os

from django.http import HttpResponse, Http404
from django.views.generic import TemplateView, DetailView
from django.shortcuts import get_object_or_404, redirect, render
from haystack.views import SearchView

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

import apps.bookrepo.models as bm
from apps.bookreader.models import BookHistory, Book, FavoriteBook, BookShelf, UsersShelves, Report, Reviews


class BookListView(TemplateView):
    template_name = 'bookrepo/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books'] = paginate(self.get_books(), self.request.GET.get("page", 1), 18, settings.MAX_PAGING_LINKS)
        return context

    @staticmethod
    def get_books():
        return bm.Book.objects.all()


class BookDetailView(DetailView):
    model = bm.Book

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        book_identifier = self.kwargs['book_identifier']
        book = Book.objects.get(identifier=book_identifier)
        context['book_identifier'] = self.kwargs['book_identifier']
        if self.request.user.is_authenticated():
            context['bookshelves'] = BookShelf.objects.filter(user=self.request.user)
        try:
            context['favorite'] = FavoriteBook.objects.get(book_identifier=book, user=self.request.user)
            context['usershelves'] = UsersShelves.objects.filter(user=self.request.user, book=book)
        except:
            context['favorite'] = None
            context['usershelves'] = None
        try:
            context['reported'] = Report.objects.get(user=self.request.user, book=book, fixed=False)
        except:
            context['reported'] = None
        context['reviews'] = Reviews.objects.filter(book_identifier=book)

        return self.render_to_response(context)

    def get_object(self, queryset=None):
        # Saves to user's history
        book_identifier = self.kwargs['book_identifier']
        book = Book.objects.get(identifier=book_identifier)
        if self.request.user.is_authenticated():
            if not BookHistory.objects.filter(book_identifier=book, user=self.request.user):
                BookHistory.objects.create(book_identifier=book, user=self.request.user)
        return get_object_or_404(self.model, identifier=self.kwargs['book_identifier'])


class BookPageView(DetailView):
    model = bm.BookPage

    def get_context_data(self, **kwargs):
        context = super(BookPageView, self).get_context_data(**kwargs)
        context['book'] = context['bookpage'].book
        return context


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
        book = get_object_or_404(bm.Book, identifier=book_identifier)
        book_page = get_object_or_404(bm.BookPage, book=book, num=page_number)
        return serve_jpg(book_page._jpg_pathname)
        # raise Http404


def serve_jpg(pathname):
    """
    Return the jpg image in a response
    """
    if os.path.exists(pathname):
        with open(pathname, 'rb') as f:
            response = HttpResponse(f.read())
            response['Content-Disposition'] = 'inline;filename={0}'.format(os.path.basename(pathname))
            return response
    else:
        raise Http404


class BookSubjectListView(TemplateView):
    template_name = 'bookrepo/book_list_subject.html'

    def get_context_data(self, **kwargs):
        context = super(BookSubjectListView, self).get_context_data(**kwargs)

        context['subjects'] = bm.Subject.objects.all()
        # subjects = bm.Subject.objects.all()
        # for subj in subjects:
        #     context['books'] = bm.Book.objects.filter(subject=subj)
        # context['books'] = paginate(self.get_books(), self.request.GET.get("page", 1), 20, settings.MAX_PAGING_LINKS)
        context['books'] = bm.Book.objects.all()
        return context

    @staticmethod
    def get_books():
        return bm.Book.objects.filter(subject=1)


def subject_books(request, subject_identifier):
    books = Book.objects.filter(subject_id=subject_identifier)
    title = bm.Subject.objects.get(id=subject_identifier)
    data = {'books': books, 'title': title}
    return render(request, 'bookrepo/book_detail_subject.html', data)

