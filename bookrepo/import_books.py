"""
Scan and update db with new books, updates existing books
"""
import os
import shutil
import glob
from zipfile import ZipFile
import tempfile
import subprocess
import csv
import re

from bs4 import BeautifulSoup

from mezzanine.conf import settings

import bookrepo.models as bm


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

        def get_text(att, default=None):
            try:
                text = getattr(getattr(xml, att), 'text')
                if text:
                    return text
                else:
                    return default
            except AttributeError:
                return default

        if xml.imagecount.text:
            num_leafs = int(xml.imagecount.text)
        else:
            # count them :(
            num_leafs = len(os.listdir(os.path.join(
                book_folder,
                jp2_folder(book_identifier))))
        return dict(
            identifier=book_identifier,
            title=get_text('title'),
            creator=get_text('creator', 'Unknown'),
            contributor=get_text('contributor', 'Unknown'),
            published=get_text('date', ''),
            subject=get_text('subject', 'Unspecified'),
            num_pages=num_leafs,
            reference=None)


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


def _migrate_scandata():
    """
    Copy existing book scandata into media
    :return:
    """
    for source_book_folder, dirnames, filenames in os.walk('/home/paul/wk/snac/source_materials/existing_books'):
        if is_source_book_folder(source_book_folder, filenames):
            book_identifier = os.path.basename(source_book_folder)
            print(book_identifier)
            target_book_folder = os.path.join(settings.BOOKS_ROOT, book_identifier)
            if not os.path.isdir(target_book_folder):
                os.mkdir(target_book_folder)

            target_scandata_pname = os.path.join(target_book_folder, 'scandata.xml')
            possible_sources = glob.glob(os.path.join(source_book_folder, '*scandata.xml'))

            if possible_sources:
                source_scandata_pname = possible_sources[0]
                shutil.copyfile(source_scandata_pname, target_scandata_pname)
            else:
                # If there is a scandata.zip, unzip it and use that
                scandata_zip_pname = os.path.join(source_book_folder, 'scandata.zip')
                if os.path.exists(scandata_zip_pname):
                    with ZipFile(scandata_zip_pname) as f:
                        f.extract('scandata.xml', target_book_folder)


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




thumbnail_page = {
    u'annexationofpunj00econuoft': 5,
    u'bandabraveorlife00soha': 7,
    u'catalogueofcoins01lahouoft': 5,
    u'crisisinpunjabfr00coop': 7,
    u'gurugobindsingh00sher': 9,
    u'gurunanaklifeand00singuoft': 7,
    u'inthesikhsanct00vaswuoft': 3,
    u'lawrencesofpunja01gibb': 11,
    u'originofsikhpowe00prinuoft': 7,
    u'panjabcastes00ibbe': 9,
    u'plantsofpunjabde00bamb': 11,
    u'punjab': 7,
    u'punjabimusalmans00wikeuoft': 5,
    u'ranjitsinghsikh00grif': 11,
    u'shorthistoryofsi00paynrich': 7,
    u'sikhsofpunjab00parruoft': 9,
    u'talesofpunjabtol00stee': 9,
    u'workingplanforch00punjrich': 1}


def _add_thumbnail_covers():
    """
    Create initial thumbnail covers for existing scanned books
    :return:
    """
    from bookrepo.models import page_jpg_path

    def add_thumbnail_cover(book_folder):
        book_identifier = os.path.basename(book_folder)
        thumbnail_path = bm.thumbnail_jpg_path(book_identifier)
        jpg_page_path = page_jpg_path(book_identifier, thumbnail_page[book_identifier])  # we know it exists
        subprocess.call(['convert', jpg_page_path, '-resize', '150x225', thumbnail_path])
        return thumbnail_path

    return list(map_book_folders(function=add_thumbnail_cover))


def _make_page_dict():
    """
    Make a starting page dictionary - one off.
    :return:
    """

    def _make_dict_tuple(book_folder):
        book_identifier = os.path.basename(book_folder)
        return book_identifier, 1

    return dict(list(map_book_folders(function=_make_dict_tuple)))


def import_scanned_books():
    """
    Import the scanned books into the ORM
    :return:
    """
    def import_scanned_book(book_folder):
        meta_info = get_book_meta_data(book_folder)
        meta_info['scanned'] = True
        return update_orm_book(meta_info)

    return list(map_book_folders(function=import_scanned_book))


def map_csv_row(row):
    csv_map = {
        'Title': 'title',
        'Author': 'creator',
        'ReferenceNo': 'reference',
        'PublishDate': 'published',
        'Pages': 'num_pages',
        'Copies': 'num_copies'}
    return {csv_map[k]: row[k] for k in csv_map}


def import_book_csv(path):
    """
    Import specified book csv
    :param path:
    :return:
    """
    with open(path, 'rb') as f:
        reader = csv.DictReader(f)
        for row in reader:
            meta_info = map_csv_row(row)

            if row['Subtitle']:
                meta_info['title'] = '{0}: {1}'.format(
                    meta_info['title'],
                    row['Subtitle'])

            matching_books = bm.Book.objects.filter(
                title=meta_info['title'],
                creator__name=meta_info['creator'])

            num_matches = matching_books.count() if matching_books else 0

            if num_matches == 0:
                meta_info['identifier'] = create_book_identifier(meta_info)
                update_orm_book(meta_info)
            elif num_matches == 1:
                update_orm_book(meta_info, matching_books[0])
            else:
                raise Exception('Multiple matching books for "{0}"'.format(meta_info['title']))


def create_book_identifier(meta_info):
    """
    Create a new identifier suitable for use as a unique folder name
    :param meta_info:
    :return:
    """
    title_part = _book_identifier_part(meta_info['title'])
    creator_part = _book_identifier_part(meta_info['creator'])
    number = 0
    while True:
        identifier = '{0}{1:>02}{2}'.format(title_part, number, creator_part)

        try:
            bm.Book.objects.get(identifier=identifier)
        except bm.Book.DoesNotExist:
            return identifier

        number += 1
        if number > 99:
            raise Exception('99 similar books!?')


def _book_identifier_part(s):
    """
    Return up to 12 characters of s made up of non common words
    :param s:
    :return:
    """
    common_words = [
        'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have', 'I', 'it', 'for', 'not',
        'on', 'with', 'he', 'as', 'you', 'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they', 'we', 'say', 'her',
        'she', 'or', 'an', 'will', 'my', 'one', 'all', 'would', 'there', 'their', 'what', 'so', 'up',
        'out', 'if', 'about', 'who', 'get', 'which', 'go', 'when', 'make', 'can', 'like', 'time',
        'no', 'just', 'him', 'know', 'take', 'person', 'into', 'year', 'your', 'good', 'some', 'could',
        'them', 'see', 'other', 'tan', 'then', 'now', 'look', 'only', 'come', 'its', 'over', 'think', 'also',
        'back', 'after', 'use', 'two', 'how', 'our', 'work', 'first', 'well', 'way', 'even',
        'want', 'because', 'any', 'these', 'give', 'day', 'us']

    s = re.sub(r'\W+', '', s)  # Removes any punctuation

    words = [w.lower() for w in s.split()]
    words = [w for w in words if w not in common_words]
    word_string = ''.join(words)
    return word_string[:12]


def update_orm_book(meta_info, book=None, redo_ocr=False):
    """
    Update orm_book, creating it if necessary.
    Also update the book pages, creating them as necessary.
    :param meta_info:
    :param book: book object, if already known
    :return: None
    """

    # Sort out foreign key objects
    for attr, model_class in (('creator', bm.Creator),
                              ('contributor', bm.Contributor),
                              ('subject', bm.Subject)):
        try:
            value_str = meta_info.pop(attr)
            if value_str:
                value_obj, created = model_class.objects.get_or_create(name=value_str)
                if created:
                    value_obj.save()
                meta_info[attr] = value_obj
        except KeyError:
            pass

    # Sort out numbers
    for attr, default in (('num_pages', 0), ('num_copies', 1)):
        if attr in meta_info:
            try:
                meta_info[attr] = int(meta_info[attr])
            except ValueError:
                meta_info[attr] = default

    if book is None:
        book, created = bm.Book.objects.get_or_create(identifier=meta_info['identifier'], defaults=meta_info)
    else:
        created = False

    if not created:
        for attr, value in meta_info.iteritems():
            setattr(book, attr, value)
    book.save()

    update_orm_book_pages(book, redo_ocr)

    return book


def get_scanned_page_start(book_folder):
    """
    Return the starting page if specified in scandata.xml (which may not be present)
    Returns zero if it can't find a number or scandata.xml
    :param book_folder: string
    :return: integer
    """
    try:
        scandata_pname = os.path.join(book_folder, 'scandata.xml')
        with open(scandata_pname) as f:
            scandata = BeautifulSoup(f, 'xml')
            return int(scandata.find('pageType', text='Title').parent['leafNum'])
    except (IOError, AttributeError, KeyError):
        return 1


def update_orm_scanned_start_pages():
    def update_orm_scanned_page(book_folder):
        book_identifier = os.path.basename(book_folder)
        book_start = get_scanned_page_start(book_folder)
        return book_identifier, book_start
    return list(map_book_folders(function=update_orm_scanned_page))


def update_orm_book_pages(book, redo_ocr=False):
    """
    Update or add the required book page objects, scanning if necessary (which creates the jpg pages)
    This could take a while.
    :param book:
    :param redo_ocr:
    :return:
    """
    for page_number in range(book.num_pages):
        page, created = bm.BookPage.objects.get_or_create(book=book, num=page_number)
        if created or redo_ocr:
            page.update_text_from_image()
            page.save()