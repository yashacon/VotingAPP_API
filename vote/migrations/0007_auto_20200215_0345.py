# Generated by Django 3.0.3 on 2020-02-14 22:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_voted_voted_item'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Voted',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='has_voted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='voted_item',
            field=models.CharField(default='none', max_length=200),
        ),
    ]