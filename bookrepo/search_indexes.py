from haystack import indexes

import bookrepo.models as bm


class BookPageIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    # ebook = indexes.BooleanField(model_attr=True, default=False)

    def get_model(self):
        return bm.BookPage