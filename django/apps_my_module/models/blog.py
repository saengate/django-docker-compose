from django.db import models

from apps_my_module.models.comments import Comments


class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
    comments = models.ForeignKey(
        Comments,
        on_delete=models.CASCADE,
        related_name='blog',
        null=True,
    )

    def __str__(self):
        return self.name
