"""
Scan and update db with new books, updates existing books
"""
import os
import shutil
from zipfile import ZipFile
import tempfile

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
    :return: list of function results
    """
    if path is None:
        path = settings.BOOKS_ROOT

    if function is None:

        def return_identity(book_dir):
            return os.path.basename(book_dir)

        function = return_identity

    return (function(dirpath) for dirpath, _, filenames in os.walk(path)
            if is_book_folder(dirpath, filenames))


def get_book_meta_data(book_folder=None, book_identifier=None):
    """
    Return a dict containing basic book info - this will be replaced by a model or some such.
    Either book_folder or book_identifier must be supplied
    :param book_folder: string
    :param book_identifier: string
    :return: dict
    """
    if book_folder is None and book_identifier is None:
        raise Exception('Both args None for get_book_meta_data')

    if book_folder is None:
        book_folder = os.path.join(settings.BOOKS_ROOT, book_identifier)
    elif book_identifier is None:
        book_identifier = os.path.basename(book_folder)

    with open(os.path.join(book_folder, meta_file_bname(book_identifier)), 'r') as f:
        xml = BeautifulSoup(f, 'xml')
        if xml.imagecount.text:
            num_leafs = int(xml.imagecount.text)
        else:
            # count them :(
            num_leafs = len(os.listdir(os.path.join(
                book_folder,
                jp2_folder(book_identifier))))
        return dict(
            identifier=book_identifier,
            title=xml.title.text,
            creator=xml.creator.text,
            date=xml.date.text,
            num_leafs=num_leafs)


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


def _fix_mispelled_jp2s():
    """
    One off - some of the jp2 files have the wrong spelling!! correct them using the book identifier
    :return:
    """
    def fix_spellings(book_folder):
        book_identifier = os.path.basename(book_folder)
        jp2_folder_path = os.path.join(book_folder, jp2_folder(book_identifier))
        for jp2_name in os.listdir(jp2_folder_path):
            if book_identifier not in jp2_name:
                old_path = os.path.join(jp2_folder_path, jp2_name)
                new_path = os.path.join(jp2_folder_path, book_identifier+jp2_name[-9:])
                shutil.move(old_path, new_path)

    return list(map_book_folders(function=fix_spellings))