from django.db import models


# Create your models here.
class UserDetails(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)


class ToolRating(models.Model):
    email = models.EmailField()
    ai_tool = models.CharField(max_length=15)
    star_rating = models.IntegerField()


class AiTool(models.Model):
    ai_tool = models.CharField(max_length=15)
    type = models.CharField(max_length=10)
    description = models.CharField(max_length=50)
    logo = models.ImageField(upload_to="static/logo")
    affiliate_link = models.BooleanField()
    webiste_url = models.URLField()
