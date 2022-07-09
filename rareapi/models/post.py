from django.db import models
from django.contrib.auth.models import User
from rareapi.models.category import Category


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.ImageField(upload_to="images")
    content = models.CharField(max_length=400)
    approved = models.BooleanField(default=True)