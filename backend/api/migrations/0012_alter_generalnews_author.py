# Generated by Django 5.0.7 on 2024-07-25 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_basictickerdata_updated_at_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='generalnews',
            name='author',
            field=models.TextField(),
        ),
    ]
