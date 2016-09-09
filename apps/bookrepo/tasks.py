#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import subprocess
import sys, os
import re
import pyPdf

from datetime import timedelta
from django.conf import settings
from celery import Celery, task
from haystack.management.commands import update_index

from .models import Book, BookPage


app = Celery('tasks')

common_words = [
    'the', 'and', 'while', 'very', 'that', 'have', 'shall', 'for', 'not', 'strike', 'death', 'The',
    'with', 'you', 'this', 'but', 'his', 'from', 'they', 'say', 'return', 'move', 'gold', 'Them', 'country',
    'will', 'one', 'all', 'would', 'there', 'their', 'what', 'What', 'great', 'They', 'Shall', 'she is',
    'out', 'about', 'who', 'get', 'which', 'when', 'make', 'can', 'like', 'time', 'head', 'Sikh', 'hero',
    'just', 'him', 'know', 'take', 'person', 'into', 'year', 'your', 'good', 'some', 'could', 'he is',
    'them', 'see', 'other', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also', 'Such',
    'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even', 'self', 'Full', 'much'
    'want', 'because', 'any', 'these', 'give', 'day', 'shot', 'blood', 'Punjab', 'It', 'gate', 'There']


def get_pdf_content(book, pages):
    path = os.path.join('%s/books/%s/') % (settings.MEDIA_ROOT, book.identifier)
    for p in os.listdir(path):
        if p.endswith('pdf'):
            pdf_file = os.path.join(path, p)
            pdf = pyPdf.PdfFileReader(file(pdf_file, "rb"))
            for i in range(0, pages):
                page, created = BookPage.objects.get_or_create(book=book, num=i)
                if created:
                    content = pdf.getPage(i).extractText() + "\n"
                    splitted = re.findall('[A-Z][^A-Z]*', content)
                    content = ' '.join(splitted)
                    for c in common_words:
                        content = content.replace(c, ' ' + c + ' ')
                        print(content)
                    try:
                        content = content.decode('utf-8').encode('utf-8')
                        cleaned_content = " ".join(content.replace("\xa0", " ").strip().split())
                    except UnicodeEncodeError:
                        cleaned_content = content
                    page.text = cleaned_content
                    page.save()
    book.num_pages = pages
    book.ebook = True
    book.scanned = True
    book.save()


def rename_files(book, jp2_path, jpg_path):
    jp_correct_names = False
    jp2_folder_has_files = False
    for f in os.walk(jp2_path):
        if f[2]:
            jp2_folder_has_files = True
            file_pattern = '%s_0000.jp2' % book.identifier
            if file_pattern in f[2]:
                jp_correct_names = True

    if not jp_correct_names and jp2_folder_has_files:
        for fname in os.listdir(jp2_path):
            name_to_replace = fname.split('_')[0]
            setting_identifier = fname.replace(name_to_replace, str(book.identifier))
            os.rename(os.path.join(jp2_path, fname), os.path.join(jp2_path, setting_identifier))

    jpgs_has_correct_names = False
    jpgs_folder_has_files = False
    for f in os.walk(jpg_path):
        if f[2]:
            jpgs_folder_has_files = True
            file_pattern = '%s_0000.jpg' % book.identifier
            if file_pattern in f[2]:
                jpgs_has_correct_names = True

    if not jpgs_has_correct_names and jpgs_folder_has_files:
        i = 0
        for f_name in os.listdir(jpg_path):
            name_to_replace = f_name.split('.jpg')[0]
            image_num = '%s_%s' % (str(book.identifier), str(i).zfill(4))
            setting_identifier = f_name.replace(name_to_replace, image_num)
            os.rename(os.path.join(jpg_path, f_name), os.path.join(jpg_path, setting_identifier))
            i += 1


def count_pages(book_id):
    b = Book.objects.get(id=book_id)
    path = os.path.join('%s/books/%s/jpgs/') % (settings.MEDIA_ROOT, b.identifier)
    path, dirs, files = os.walk(path).next()
    if len(files):
        b.num_pages = len(files)
        b.save()
    return len(files)


@task.periodic_task(run_every=timedelta(minutes=5))
def get_book_ocr():
    if settings.USE_CELERY:
        return run_get_book_ocr()


@task.periodic_task(run_every=timedelta(hours=1))
def update_haystack_index():
    update_index.Command().handle()


def run_get_book_ocr():
    unprocessed_books = Book.objects.filter(scanned=False)
    for book in unprocessed_books:
        fullpath = os.path.join('%s/books/%s/') % (settings.MEDIA_ROOT, book.identifier)
        jp2_path = os.path.join(fullpath, 'jp2')
        jpg_path = os.path.join(fullpath, 'jpgs')

        if not os.path.exists(jp2_path):
            os.makedirs(jp2_path)
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)

        jpg_folder_is_empty = True
        path, dirs, files = os.walk(jpg_path).next()
        if files:
            jpg_folder_is_empty = False

        is_pdf = False
        for p in os.listdir(fullpath):
            if p.endswith('pdf'):
                is_pdf = True
                if jpg_folder_is_empty:
                    subprocess.call(['convert', os.path.join(fullpath, p), '-resize', '3840x2160',
                                     os.path.join(jpg_path, '0.jpg')])

        convert_jp2_to_jpg(jp2_path, jpg_path)
        rename_files(book, jp2_path, jpg_path)
        pages = count_pages(book.id)

        if is_pdf:
            if book.is_panjabi:
                for page_number in range(pages + 1):
                    page, created = BookPage.objects.get_or_create(book=book, num=page_number)
                    if created:
                        try:
                            page.update_punjabi_text_from_image()
                            page.save()
                        except IOError:
                            print(' > Unable to scan Punjabi {title} - page {page_number}'.format(
                                title=book.title,
                                page_number=page_number))

            else:
                get_pdf_content(book, pages)
        else:
            text_from_image(book, pages)


def text_from_image(book, pages):
    if pages:
        for page_number in range(pages + 1):
            page, created = BookPage.objects.get_or_create(book=book, num=page_number)
            if created:
                if book.is_panjabi:
                    try:
                        page.update_punjabi_text_from_image()
                        page.save()
                    except IOError:
                        print(' > Unable to scan Punjabi {title} - page {page_number}'.format(
                            title=book.title,
                            page_number=page_number))
                else:
                    try:
                        page.update_text_from_image()
                        page.save()
                    except IOError:
                        print(' > Unable to scan English {title} - page {page_number}'.format(
                            title=book.title,
                            page_number=page_number, ))
        book.num_pages = pages
        book.scanned = True
        book.ebook = True
        book.save()


def convert_jp2_to_jpg(jp2_path, jpg_path):
    jpg_folder_is_empty = True
    path, dirs, files = os.walk(jpg_path).next()
    if files:
        jpg_folder_is_empty = False

    for p in os.listdir(jp2_path):
        if jpg_folder_is_empty:
            try:
                subprocess.call(['convert', os.path.join(jp2_path, p), '-resize', '2048x1152',
                                 os.path.join(jpg_path, '0.jpg')])
            except Exception as e:
                print(e)

