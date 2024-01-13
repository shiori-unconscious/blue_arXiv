from django.db import models
from django.contrib.auth import get_user_model


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, db_index=True)

    def __str__(self):
        return self.name
    
class Paper(models.Model):
    arxiv_id = models.CharField(max_length=50, unique=True, db_index=True)
    authors = models.CharField(max_length=100, null=True)
    title = models.CharField(max_length=255)
    doi = models.URLField(blank=True, null=True)
    abstract = models.TextField()
    categories = models.ManyToManyField(Category)
    upload_time = models.DateTimeField()
        
    def __str__(self) -> str:
        return self.title
