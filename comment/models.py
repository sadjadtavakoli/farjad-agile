from django.db import models

from farjad.utils.utils_view import get_url


class Comment(models.Model):
    date = models.DateField()
    likes=models.IntegerField()
    text = models.CharField(max_length=5000,null=False)
    writer = models.ForeignKey("members.Member", related_name="comments", on_delete=models.DO_NOTHING)
    book = models.ForeignKey("books.Books", related_name="comments", on_delete=models.DO_NOTHING)
