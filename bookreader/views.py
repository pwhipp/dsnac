from random import randint
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core import serializers

from bookrepo.models import Book

from bookreader.models import BookReading, BookHistory, FavoriteBook, BookShelf, UsersShelves, Report


class BookReaderView(TemplateView):
    template_name = 'bookreader/reader.html'

    def get_context_data(self, **kwargs):
        context = super(BookReaderView, self).get_context_data(**kwargs)
        book_identifier = self.kwargs['book_identifier']
        page_num = self.kwargs['page_num']
        context['start_page'] = page_num
        context['book'] = Book.objects.get(identifier=book_identifier)

        # Saving books to Reading table
        if not BookReading.objects.filter(book_identifier=context['book'],  user=self.request.user):
            BookReading.objects.create(book_identifier=context['book'], user=self.request.user)

        context['book_json'] = serializers.serialize('json', [context['book']])[1:-2]
        return context


class UsersBooks(TemplateView):
    template_name = 'usersbook.html'

    def get_context_data(self, **kwargs):
        context = super(UsersBooks, self).get_context_data(**kwargs)
        br = BookReading.objects.filter(user=self.request.user).values_list('book_identifier')
        context['books'] = Book.objects.filter(id__in=br)
        context['title'] = 'Reading'
        return context


class UsersHistory(UsersBooks):

    def get_context_data(self, **kwargs):
        context = super(UsersHistory, self).get_context_data(**kwargs)
        br = BookHistory.objects.filter(user=self.request.user).values_list('book_identifier')
        context['books'] = Book.objects.filter(id__in=br)
        context['title'] = 'My History'
        return context


class UsersFavorite(UsersBooks):

    def get_context_data(self, **kwargs):
        context = super(UsersFavorite, self).get_context_data(**kwargs)
        br = FavoriteBook.objects.filter(user=self.request.user).values_list('book_identifier')
        context['books'] = Book.objects.filter(id__in=br)
        context['title'] = 'My Favorites'
        return context


def favorite_book(request, book_identifier):
    # if request.POST:
        book = Book.objects.get(identifier=book_identifier)
        FavoriteBook.objects.create(book_identifier=book, user=request.user)
        return redirect('bookrepo_detail', book_identifier=book.identifier)


# fixme make a class based view
# class UsersShelves(TemplateView):
#     template_name = 'shelf.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(UsersShelves, self).get_context_data(**kwargs)
#         br = FavoriteBook.objects.filter(user=self.request.user).values_list('book_identifier')
#         context['books'] = Book.objects.filter(id__in=br)
#         context['title'] = 'My Shelf'
#         return context
#
#     def post(self, request, *args, **kwargs):
#         a = request.POST.get('shelf_name', '')
#         print a
#         return self.get(request, *args, **kwargs)
#         # return HttpResponseRedirect(reverse('bookshelf'))


def bookshelf(request):
    """
    Adding new bookshelves
    if input is empty - it's generates name 'BookShelf_<random_num>'
    :param request:
    :return:
    """
    if request.POST:
        shelf_name = request.POST.get('shelf_name', '')
        if shelf_name:
            BookShelf.objects.create(name=shelf_name, user=request.user)
        else:
            shelf_name = 'MyBookShelf_%s' % randint(0, 99)
            BookShelf.objects.create(name=shelf_name, user=request.user)

        return HttpResponseRedirect(reverse('bookshelf'))
    else:
        books = BookShelf.objects.filter(user=request.user)
        data = {'books': books}
        return render(request, 'add_shelf.html', data)


def my_shelves(request):
    """
    list of books in one page
    :param request:
    :return:
    """
    shelves = UsersShelves.objects.filter(user=request.user).order_by('-added')
    books_count = UsersShelves.objects.filter(user=request.user).count()
    data = {'shelves': shelves, 'books_count': books_count}
    return render(request, 'shelf.html', data)


def add_book_bookshelf(request):
    """
    adding book to a selected bookshelf
    :param request:
    :return:
    """
    if request.POST:
        book_id = request.POST.get('book', '')
        shelf_id = request.POST.get('selectshelf', '')
        shelf = BookShelf.objects.get(id=shelf_id)
        book = Book.objects.get(id=book_id)
        book_in_shelf = UsersShelves.objects.filter(user=request.user, book=book, shelf=shelf).count()
        if not book_in_shelf:
            UsersShelves.objects.create(user=request.user, book=book, shelf=shelf)
        return redirect('mybookshelf')


def report_problem(request):
    if request.POST:
        book_id = request.POST.get('book', '')
        book = Book.objects.get(id=book_id)
        Report.objects.create(user=request.user, book=book)
        return redirect('bookrepo_detail', book_identifier=book.identifier)

from django import forms
from haystack.forms import SearchForm


class EbookSearchForm(SearchForm):
    q = forms.CharField(required=False)
    ebook = forms.BooleanField(required=False)

    def search(self):
        sqs = super(EbookSearchForm, self).search()
        if self.is_valid() and self.cleaned_data['ebook']:
            sqs = sqs.filter(ebook=True)

        return sqs