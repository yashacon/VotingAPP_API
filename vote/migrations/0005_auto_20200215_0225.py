# Generated by Django 3.0.3 on 2020-02-14 20:55

from django.db import migrations, models
import vote.models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='display_picture',
            field=models.ImageField(upload_to=vote.models.get_upload_path),
        ),
    ]
