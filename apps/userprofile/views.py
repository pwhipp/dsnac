from django.shortcuts import render
from apps.donate.models import Donate
from apps.bookreader.models import FavoriteBook, BookReading
from django.db.models import Sum


def dashboard(request):
    if request.user.is_authenticated():
        user = request.user
        transactions = Donate.objects.filter(user=user.profile)
        favorite_books = FavoriteBook.objects.filter(user=user)
        total = Donate.objects.filter(user=user.profile).aggregate(Sum('amount'))
        reading = BookReading.objects.filter(user=user)
        data = {
            'user': user,
            'transactions': transactions,
            'favorite_books': favorite_books,
            'total': total,
            'reading': reading
        }
        return render(request, 'dashboard.html', data)
    return render(request, 'dashboard.html', {})
