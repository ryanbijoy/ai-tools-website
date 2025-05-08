from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class ToolRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    ai_tool = models.CharField(max_length=15)
    star_rating = models.IntegerField(null=True, default=None)
    review = models.TextField(null=True, default=None)

    def __str__(self):
        return f"Review by {self.user} for {self.ai_tool}"


class Category(models.Model):
    title = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class AiTool(models.Model):
    category = models.ManyToManyField(Category, blank=True, related_name="toolcategory")
    category_display = models.CharField(max_length=50, null=True)
    ai_tool = models.CharField(max_length=50)
    description = models.TextField()
    media_link = models.URLField()
    website_url = models.URLField()
    logo = models.CharField(max_length=50, blank=True, null=True)
    about = models.TextField()
    features = models.JSONField(default=dict)
    tags = models.JSONField(default=list, blank=True)
    affiliate_link = models.BooleanField(default=False)

    def __str__(self):
        return self.ai_tool

    def avg_rating(self):
        return ToolRating.objects.filter(ai_tool=self).aggregate(Avg('star_rating'))['star_rating__avg'] or 0

    def total_votes(self):
        return ToolRating.objects.filter(ai_tool=self).count() or 0


class Testimonial(models.Model):
    full_name = models.CharField(max_length=25)
    photo_url = models.CharField(max_length=25)
    testimonial = models.CharField(max_length=150)

    def __str__(self):
        return self.full_name
