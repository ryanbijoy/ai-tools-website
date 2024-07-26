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
    ai_tool = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    description = models.CharField()
    logo = models.CharField(max_length=50)
    affiliate_link = models.BooleanField(default=False)
    website_url = models.URLField(blank=True)

    def __str__(self):
        return self.ai_tool
