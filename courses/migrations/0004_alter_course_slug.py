# Generated by Django 5.0.6 on 2024-06-05 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0003_course_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(default='', unique=True),
        ),
    ]
