# Generated by Django 3.2.18 on 2023-04-23 18:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bike', '0003_auto_20230423_0243'),
        ('rent', '0003_auto_20230423_2316'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rentreview',
            name='rent',
        ),
        migrations.AddField(
            model_name='rentreview',
            name='bike',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rent_review_bike', to='bike.bike'),
            preserve_default=False,
        ),
    ]
