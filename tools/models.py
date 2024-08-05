from django.db import models
from django.contrib.auth.models import User


class ToolRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    ai_tool = models.CharField(max_length=15)
    star_rating = models.IntegerField(null=True, default=None)
    review = models.TextField(null=True, default=None)

    def __str__(self):
        return f"Review by {self.user} for {self.ai_tool}"


class AiTool(models.Model):
    ai_tool = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    media_link = models.URLField()
    website_url = models.URLField()
    logo = models.CharField(max_length=50, blank=True, null=True)
    about = models.CharField(max_length=250)
    features = models.JSONField(max_length=250)
    affiliate_link = models.BooleanField(default=False)

    def __str__(self):
        return self.ai_tool


class Testimonial(models.Model):
    full_name = models.CharField(max_length=25)
    photo_url = models.CharField(max_length=25)
    testimonial = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name
