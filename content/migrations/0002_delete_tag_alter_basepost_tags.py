# Generated by Django 4.2.1 on 2023-06-01 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0002_tag'),
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Tag',
        ),
        migrations.AlterField(
            model_name='basepost',
            name='tags',
            field=models.ManyToManyField(to='community.tag'),
        ),
    ]