from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core import serializers

from bookrepo.models import Book

from bookreader.models import BookReading, BookHistory, FavoriteBook


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
