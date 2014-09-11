from django.http import HttpResponse, HttpResponseNotFound


def page(request, book_name, page_number):
    return HttpResponse('<h1>{book_name}</h1><h2>{page_number}</h2>'.format(
        book_name=book_name,
        page_number=page_number))
