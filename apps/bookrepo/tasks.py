from __future__ import absolute_import

import subprocess
import sys, os
from datetime import timedelta
from django.conf import settings
from celery import Celery, task

from .models import Book, BookPage


app = Celery('tasks')


def rename_files(book, jp2_path, jpg_path):
    jp_correct_names = False
    for f in os.walk(jp2_path):
        if f:
            file_pattern = '%s_0000.jp2' % book.identifier
            if file_pattern in f[2]:
                jp_correct_names = True

    if not jp_correct_names:
        for fname in os.listdir(jp2_path):
            name_to_replace = fname.split('_')[0]
            setting_identifier = fname.replace(name_to_replace, str(book.identifier))
            os.rename(os.path.join(jp2_path, fname), os.path.join(jp2_path, setting_identifier))

    jpgs_has_correct_names = False
    for f in os.walk(jpg_path):
        if f:
            file_pattern = '%s_0000.jpg' % book.identifier
            if file_pattern in f[2]:
                jpgs_has_correct_names = True

    if not jpgs_has_correct_names:
        i = 0
        for f_name in os.listdir(jpg_path):
            name_to_replace = f_name.split('.jpg')[0]
            image_num = '%s_%s' % (str(book.identifier), str(i).zfill(4))
            setting_identifier = f_name.replace(name_to_replace, image_num)
            os.rename(os.path.join(jpg_path, f_name), os.path.join(jpg_path, setting_identifier))
            i += 1


def count_pages(book_id):
    num_pages = 0
    b = Book.objects.get(id=book_id)
    path = os.path.join('%s/books/%s/jpgs/') % (settings.MEDIA_ROOT, b.identifier)
    path, dirs, files = os.walk(path).next()
    if len(files):
        b.num_pages = len(files)
        b.save()
    return len(files)


@task.periodic_task(run_every=timedelta(seconds=5))
def get_book_ocr():
    if settings.USE_CELERY:
        return run_get_book_ocr()


def run_get_book_ocr():
    unprocessed_books = Book.objects.filter(scanned=False)
    for book in unprocessed_books:
        fullpath = os.path.join('%s/books/%s/') % (settings.MEDIA_ROOT, book.identifier)
        jp2_path = os.path.join(fullpath, 'jp2')
        jpg_path = os.path.join(fullpath, 'jpgs')

        convert_pdf_to_jpg(fullpath, jpg_path)
        convert_jp2_to_jpg(jp2_path, jpg_path)
        rename_files(book, jp2_path, jpg_path)
        pages = count_pages(book.id)
        text_from_image(book, pages)


def text_from_image(book, pages):
    if pages:
        for page_number in range(pages + 1):
            page, created = BookPage.objects.get_or_create(book=book, num=page_number)
            if created:
                if book.is_panjabi:
                    try:
                        page.update_punjabi_text_from_image()
                    except IOError:
                        print('Unable to scan Punjabi {title} - page {page_number}'.format(
                            title=book.title,
                            page_number=page_number))
                else:
                    try:
                        page.update_text_from_image()
                        page.save()
                    except IOError:
                        print('Unable to scan {title} - page {page_number}'.format(
                            title=book.title,
                            page_number=page_number, ))
        book.scanned = True
        book.ebook = True
        book.save()


def convert_pdf_to_jpg(fullpath, jpg_path):
    jpg_folder_is_empty = True
    path, dirs, files = os.walk(jpg_path).next()
    if files:
        jpg_folder_is_empty = False

    for p in os.listdir(fullpath):
        if p.endswith('pdf'):
            if jpg_folder_is_empty:
                subprocess.call(['convert', os.path.join(fullpath, p), '-resize', '2048>',
                                 os.path.join(jpg_path, '0.jpg')])


def convert_jp2_to_jpg(jp2_path, jpg_path):
    jpg_folder_is_empty = True
    path, dirs, files = os.walk(jpg_path).next()
    if files:
        jpg_folder_is_empty = False

    for p in os.listdir(jp2_path):
        if jpg_folder_is_empty:
            try:
                subprocess.call(['convert', os.path.join(jp2_path, p), '-crop', '805X972+34+94>',
                                 os.path.join(jpg_path, '0.jpg')])
            except Exception as e:
                print(e)

