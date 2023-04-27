# Generated by Django 3.2.18 on 2023-04-24 17:15

from django.db import migrations
import django_resized.forms


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0003_auto_20230423_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bike',
            name='bike_photo',
            field=django_resized.forms.ResizedImageField(crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1080, 768], upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='bike_photo_1',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1080, 768], upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='bike_photo_2',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1080, 768], upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='bike_photo_3',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1080, 768], upload_to='photos/%Y/%m/%d/'),
        ),
        migrations.AlterField(
            model_name='bike',
            name='bike_photo_4',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, force_format='JPEG', keep_meta=True, quality=75, scale=None, size=[1080, 768], upload_to='photos/%Y/%m/%d/'),
        ),
    ]
