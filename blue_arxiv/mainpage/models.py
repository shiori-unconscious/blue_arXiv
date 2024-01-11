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
    # journal = models.ManyToManyField(Journal)
    doi = models.URLField(blank=True, null=True)
    abstract = models.TextField()
    categories = models.ManyToManyField(Category)
    upload_time = models.DateTimeField()
    views_count = models.IntegerField(default=0)
    recommendations_count = models.IntegerField(default=0)
        
    def __str__(self) -> str:
        return self.title

class UserActivity(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    liked_content = models.ManyToManyField(Paper, related_name='liked_by_users')
    viewed_content = models.ManyToManyField(Paper, related_name='viewed_by_users')