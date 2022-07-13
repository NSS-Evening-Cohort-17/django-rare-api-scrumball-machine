from distutils.command.upload import upload
from django.db import models
from rareapi.models.rareuser import RareUser
from rareapi.models.category import Category


class Post(models.Model):
    rareuser = models.ForeignKey(RareUser, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    publication_date = models.DateField()
    image_url = models.CharField(max_length=1000)
    content = models.CharField(max_length=400)
    approved = models.BooleanField(default=True)
    
    