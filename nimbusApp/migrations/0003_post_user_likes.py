# Generated by Django 2.2 on 2020-11-03 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nimbusApp', '0002_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='user_likes',
            field=models.ManyToManyField(related_name='liked_posts', to='nimbusApp.User'),
        ),
    ]
