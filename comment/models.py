from django.db import models


class Comment(models.Model):
    date = models.DateField()
    text = models.CharField(max_length=5000, null=False)
    writer = models.ForeignKey("members.Member", related_name="comments",
                               on_delete=models.DO_NOTHING)
    book = models.ForeignKey("books.Books", related_name="comments", on_delete=models.DO_NOTHING)
