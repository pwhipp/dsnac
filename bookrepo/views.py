from django.http import HttpResponse, Http404


def page(request, book_name, page_number):
    """
    Return the jp2 image corresponding to the specified page
    :param request: Request object
    :param book_name: The folder name being used for the book
    :param page_number: integer; 0 < page_number < 9999
    :return:
    """
    mime_type = 'image/jp2'
    file_path = get_book_page_image_file_name(book_name, page_number)
    if file_path:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), mimetype=mime_type)
            response['Content-Disposition'] = 'inline;filename={0}'.format(os.path.basename(file_path))
            return response
    else:
        raise Http404
