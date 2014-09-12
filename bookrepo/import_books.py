"""
Scan and update db with new books, updates existing books
"""
import os
import shutil
from zipfile import ZipFile
import tempfile
import sys

from bs4 import BeautifulSoup

from mezzanine.conf import settings


def meta_file_bname(book_identifier):
    """
    Return the meta xml file base name for book_identifier
    :param book_identifier:
    :return: string
    """
    return '{0}_meta.xml'.format(book_identifier)


def jp2_folder(book_identifier):
    """
    Return the jp2 zip base name for book_identifier
    :param book_identifier:
    :return: string
    """
    return '{0}_jp2'.format(book_identifier)


def is_book_folder(dirpath, filenames):
    book_identifier = os.path.basename(dirpath)
    return meta_file_bname(book_identifier) in filenames


def map_book_folders(path=None, function=None):
    """
    Import all of the books on path. books are updated by identity.
    Path is searched recursively.
    A 'book' is any folder containing a <folder_name>_meta.xml file.
    :param path: file path to books
    :return:
    """
    if path is None:
        path = settings.BOOKS_ROOT

    if function is None:

        def print_identity(book_dir):
            book_ident = os.path.basename(book_dir)
            print('found book with identifier="{0}"'.format(book_ident))

        function = print_identity

    for dirpath, dirnames, filenames in os.walk(path):
        if is_book_folder(dirpath, filenames):
            function(dirpath)


def import_book_meta_data(book_folder):
    """
    Not bothering to do this yet - Reading directly from the xml in the view context
    :param book_folder:
    :return:
    """
    book_identifier = os.path.basename(book_folder)

    with open(os.path.join(book_folder, meta_file_bname(book_identifier)), 'r') as f:
        xml = BeautifulSoup(f, 'xml')
        print(xml.title.text, xml.creator.text, xml.date.text)


def import_book_folder_meta_data(path=None):
    """
    Import all of the books on path. books are updated by identity.
    Path is searched recursively.
    A 'book' is any folder containing a <folder_name>_meta.xml file.
    :param path: file path to books
    :return:
    """
    map_book_folders(path, import_book_meta_data)


def is_source_book_folder(dirpath, filenames):
    book_identifier = os.path.basename(dirpath)
    return ((meta_file_bname(book_identifier) in filenames) and
            ('{0}_jp2.zip'.format(book_identifier) in filenames))


def _migrate_books():
    """
    Move the existing books into a more suitable format under media
    :return: None
    """
    for source_book_folder, dirnames, filenames in os.walk('/home/paul/wk/snac/source_materials/existing_books'):
        if is_source_book_folder(source_book_folder, filenames):
            book_identifier = os.path.basename(source_book_folder)
            print(book_identifier)
            book_folder = os.path.join(settings.BOOKS_ROOT, book_identifier)
            if not os.path.isdir(book_folder):
                os.mkdir(book_folder)
            shutil.copyfile(os.path.join(source_book_folder, meta_file_bname(book_identifier)),
                            os.path.join(book_folder, meta_file_bname(book_identifier)))

            # Unzip the jp2s into a temporary folder and convert them into jpgs for display
            jp2_source_dir = tempfile.mkdtemp()
            jp2_target_dir = os.path.join(book_folder, jp2_folder(book_identifier))
            if not os.path.isdir(jp2_target_dir):
                os.mkdir(jp2_target_dir)
            jpg_target_dir = os.path.join(book_folder, 'jpgs')
            if not os.path.isdir(jpg_target_dir):
                os.mkdir(jpg_target_dir)
            try:
                with ZipFile(os.path.join(source_book_folder, '{0}.zip'.format(jp2_folder(book_identifier)))) as f:
                    f.extractall(jp2_source_dir)
                for dirpath, _, jp2_filenames in os.walk(jp2_source_dir):
                    for filename in jp2_filenames:
                        basename, ext = os.path.splitext(filename)
                        if ext == '.jp2':
                            jp2_source_file_path = os.path.join(dirpath, filename)
                            jp2_target_file_path = os.path.join(jp2_target_dir, filename)
                            shutil.copyfile(jp2_source_file_path, jp2_target_file_path)
            finally:
                shutil.rmtree(jp2_source_dir)