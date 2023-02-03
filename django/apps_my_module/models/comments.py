from django.db import models


class Comments(models.Model):
    comment = models.TextField()
