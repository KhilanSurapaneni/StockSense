# Generated by Django 5.0.7 on 2024-07-22 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_detailedtickerdata_beta_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='country',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
    ]
