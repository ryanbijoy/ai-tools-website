# Generated by Django 5.0.6 on 2024-08-17 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tools", "0025_alter_aitool_category"),
    ]

    operations = [
        migrations.AlterField(
            model_name="aitool",
            name="about",
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name="aitool",
            name="description",
            field=models.CharField(max_length=300),
        ),
    ]
