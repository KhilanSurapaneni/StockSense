# Generated by Django 5.0.7 on 2024-07-22 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='beta',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='ceo',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='cik',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='city',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='country',
            field=models.CharField(blank=True, max_length=2, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='dcf',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='dcfDiff',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='defaultImage',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='fullTimeEmployees',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='isAdr',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='isEtf',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='isFund',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='range',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='sector',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='state',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='volAvg',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='website',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='detailedtickerdata',
            name='zip',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
