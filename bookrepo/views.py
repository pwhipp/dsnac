import os

from django.http import HttpResponse, Http404

from mezzanine.conf import settings


def page(request, book_name, page_number):
    """
    Return the jp2 image corresponding to the specified page
    :param request: Request object
    :param book_name: The folder name being used for the book
    :param page_number: integer; 0 < page_number < 9999
    :return:
    """
    mime_type = 'image/jpg'
    file_path = get_jpg(book_name, page_number)

    if file_path is None:
        file_path = create_jpg_from_jp2(book_name, page_number)

    if file_path:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), mimetype=mime_type)
            response['Content-Disposition'] = 'inline;filename={0}'.format(os.path.basename(file_path))
            return response
    else:
        raise Http404


def get_jpg(book_name, page_number):
    """
    Return the jpg file corresponding to the parameters. Return None if not found.
    :param book_name: string: The folder name being used for the book
    :param page_number: integer: The page number wanted
    :return: file path to the image or None
    """
    return os.path.join(settings.MEDIA_ROOT, 'uploads/books/annexationofpunj00econuoft/jpgs/annexationofpunj00econuoft_0034.jpg')


def create_jpg_from_jp2(book_name, page_number):
    """
    Create and return the jpg file corresponding to the parameters using the corresponding jp2 file if any.
    If no jp2 file is found, return None
    :param book_name: string: The folder name being used for the book
    :param page_number: integer: The page number wanted
    :return: file path to the jpg image file or None if no jp2 file was found
    """
    return os.path.join(settings.MEDIA_ROOT, 'uploads/books/annexationofpunj00econuoft/jpgs/annexationofpunj00econuoft_0034.jpg')
