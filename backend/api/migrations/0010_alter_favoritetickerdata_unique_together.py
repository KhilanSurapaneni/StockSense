# Generated by Django 5.0.7 on 2024-07-23 20:55

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_generalnews_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='favoritetickerdata',
            unique_together={('user', 'basic_data')},
        ),
    ]
