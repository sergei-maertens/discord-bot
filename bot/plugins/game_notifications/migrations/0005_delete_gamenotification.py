# Generated by Django 2.2.13 on 2020-08-02 10:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game_notifications', '0004_gamenotification_muted'),
    ]

    operations = [
        migrations.DeleteModel(
            name='GameNotification',
        ),
    ]
