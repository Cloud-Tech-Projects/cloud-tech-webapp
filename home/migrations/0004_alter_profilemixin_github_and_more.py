# Generated by Django 4.2.1 on 2023-06-15 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_rename_profile_picture_profilemixin_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemixin',
            name='github',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='profilemixin',
            name='linkedin',
            field=models.URLField(default=''),
        ),
        migrations.AlterField(
            model_name='profilemixin',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='profilemixin',
            name='twitter',
            field=models.URLField(default=''),
        ),
    ]