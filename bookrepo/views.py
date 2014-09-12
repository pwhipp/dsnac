import os
import subprocess

from django.http import HttpResponse, Http404
from django.views.generic import TemplateView

from mezzanine.conf import settings
from mezzanine.utils.views import paginate

from bookrepo.import_books import map_book_folders, get_book_meta_data


class BookListView(TemplateView):
    template_name = 'bookrepo/book_list.html'

    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['books'] = paginate(self.get_books(), self.request.GET.get("page", 1), 20, settings.MAX_PAGING_LINKS)
        return context

    @staticmethod
    def get_books():
        return list(map_book_folders(function=get_book_meta_data))


def page(request, book_identifier, page_number):
    """
    Return the jp2 image corresponding to the specified page
    :param request: Request object
    :param book_identifier: The folder name being used for the book
    :param page_number: integer; 0 < page_number < 9999
    :return:
    """
    mime_type = 'image/jpg'
    file_path = get_jpg_file_path(book_identifier, page_number)

    if file_path is None:
        file_path = create_jpg_from_jp2(book_identifier, page_number)

    if file_path:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), mimetype=mime_type)
            response['Content-Disposition'] = 'inline;filename={0}'.format(os.path.basename(file_path))
            return response
    else:
        raise Http404


def page_basename(book_identifier, page_number):
    return '{book_identifier}_{page_number:>04}'.format(
        book_identifier=book_identifier,
        page_number=page_number)


def jpg_path(book_identifier, page_number):
    return os.path.join(settings.BOOKS_ROOT,
                        book_identifier,
                        'jpgs',
                        page_basename(book_identifier, page_number)+'.jpg')


def jp2_path(book_identifier, page_number):
    return os.path.join(settings.BOOKS_ROOT,
                        book_identifier,
                        '{0}_jp2'.format(book_identifier),
                        page_basename(book_identifier, page_number)+'.jp2')


def get_jpg_file_path(book_identifier, page_number):
    """
    Return the jpg file corresponding to the parameters. Return None if not found.
    :param book_identifier: string: The folder name being used for the book
    :param page_number: integer: The page number wanted
    :return: file path to the image or None
    """
    jpg_file_path = jpg_path(book_identifier, page_number)
    if os.path.exists(jpg_file_path):
        return jpg_file_path
    else:
        return None


def create_jpg_from_jp2(book_identifier, page_number):
    """
    Create and return the jpg file corresponding to the parameters using the corresponding jp2 file if any.
    If no jp2 file is found, return None
    :param book_identifier: string: The folder name being used for the book
    :param page_number: integer: The page number wanted
    :return: file path to the jpg image file or None if no jp2 file was found
    """
    jp2_file_path = jp2_path(book_identifier, page_number)
    jpg_file_path = jpg_path(book_identifier, page_number)
    if not os.path.exists(jp2_file_path):
        print('{0} not found'.format(jp2_file_path))
        raise Http404
    if subprocess.call(['convert', jp2_file_path, '-resize', '800>', jpg_file_path]) == 0:
        return jpg_file_path
    else:
        print('{0} conversion failed'.format(jp2_file_path))
        raise Http404
