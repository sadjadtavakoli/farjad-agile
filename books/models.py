from django.db import models

from farjad.settings import PERIOD, GENRE, AGE


class Books(models.Model):
    title = models.CharField(max_length=200, blank=False, null=False)
    author = models.CharField(max_length=200, blank=False, null=False)
    pub_date = models.DateField()
    price = models.IntegerField(blank=False, null=False)
    period = models.CharField(max_length=10, choices=PERIOD)
    genre = models.CharField(max_length=10, choices=GENRE)
    reader_age = models.CharField(max_length=10, choices=AGE)
    page_num = models.IntegerField()
    length = models.IntegerField()
    width = models.IntegerField()
    jeld_num = models.IntegerField()
    description = models.CharField(max_length=1000)
    summary = models.CharField(max_length=5000)
    owner = models.ForeignKey("members.Member", related_name="books", on_delete='CASCADE')
