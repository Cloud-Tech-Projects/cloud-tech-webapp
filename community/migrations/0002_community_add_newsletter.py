# Generated by Django 4.2.1 on 2023-06-12 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='add_newsletter',
            field=models.BooleanField(default=True),
        ),
    ]
