# Generated by Django 5.0.6 on 2024-07-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0011_userdetail_is_active"),
    ]

    operations = [
        migrations.AddField(
            model_name="userdetail",
            name="username",
            field=models.CharField(default="", max_length=30),
            preserve_default=False,
        ),
    ]
