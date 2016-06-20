from haystack import indexes

import apps.bookrepo.models as bm


class BookPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)

    def get_model(self):
        return bm.BookPage