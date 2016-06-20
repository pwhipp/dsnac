from django.db import models
from mezzanine.conf import settings
import csv
from apps.bookrepo.models import Book, Creator
from django.core.exceptions import ObjectDoesNotExist
from codecs import open


class BulkUpload(models.Model):
    """
    Waiting for csv file, parse it and updating db.
    Makes book_identifier like = 'asfasf1r' w/o slashes and spaces.
    if exist:
        don't add

    """
    csv_file = models.FileField(upload_to='csv/', verbose_name='Upload a csv')
    uploaded = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'a csv file'
        verbose_name_plural = 'csv files'

    def __unicode__(self):
        return str(self.uploaded)

    def save(self, *args, **kwargs):
        super(BulkUpload, self).save(*args, **kwargs)
        dir = '%s/' % settings.MEDIA_ROOT
        filename = '%s/%s' % (dir, str(self.csv_file))

        reader = csv.reader(open(filename, 'rU', encoding='utf-7'), delimiter=',', quotechar='"')
        for row in reader:
            book = Book()
            if row[0]:
                if row[0] != 'Title':
                    identifier = ''.join(e.lower() for e in row[0] if e.isalnum())
                    try:
                        # checks if identifier is exist
                        Book.objects.get(identifier=identifier)
                    except ObjectDoesNotExist:
                        if row[0]:
                            book.title = row[0]
                            book.identifier = identifier
                        try:
                            # adding new book to existing creator
                            creator = Creator.objects.get(name=row[1])
                            book.creator = creator
                            book.reference = row[2]
                            book.published = row[3]
                            book.num_pages = row[5]
                            book.save()
                        except ObjectDoesNotExist:
                            # new book with new creator
                            creator = Creator.objects.create(name=row[1])
                            book.creator = creator
                            book.reference = row[2]
                            book.published = row[3]
                            book.num_pages = row[5]
                            book.save()