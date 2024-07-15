from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class UserDetail(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class ToolRating(models.Model):
    email = models.EmailField()
    ai_tool = models.CharField(max_length=15)
    star_rating = models.IntegerField()

    def __str__(self):
        return f'{self.email} - {self.ai_tool} - {self.star_rating}'


class AiTool(models.Model):
    ai_tool = models.CharField(max_length=25)
    type = models.CharField(max_length=25)
    description = models.CharField()
    logo = models.CharField(max_length=50)
    affiliate_link = models.BooleanField(default=False)
    website_url = models.URLField(blank=True)
    # about = models.CharField(max_length=250, null=True, default=False)
    # pricing_plans = ArrayField(
    #     models.JSONField(),
    #     default=list,
    #     null=True,
    #     help_text='Enter pricing plans as JSON objects. Example: [{"name": "Basic", "price": "$10/month", "features": "Basic features"}, ...]'
    # )

    def __str__(self):
        return self.ai_tool
