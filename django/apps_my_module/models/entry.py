from django.db import models

from apps_my_module.models.author import Author
from apps_my_module.models.blog import Blog


class Entry(models.Model):
    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name='entries',
    )
    authors = models.ManyToManyField(
        Author,
        related_name='entries',
    )
    headline = models.CharField(max_length=255)
    body_text = models.TextField()
    pub_date = models.DateField()
    mod_date = models.DateField()
    number_of_comments = models.IntegerField()
    number_of_pingbacks = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self):
        return self.headline
