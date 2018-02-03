from rest_framework.serializers import ModelSerializer

from books.models import Books


class BookSerializer(ModelSerializer):
    class Meta:
        model = Books
        # fields = ('pk', 'title', 'author','pub_date','period','price','genre','reader_age',)
        fields = ('__all__',)
