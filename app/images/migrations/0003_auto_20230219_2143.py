# Generated by Django 3.2.6 on 2023-02-19 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20230219_2030'),
    ]

    operations = [
        migrations.AddField(
            model_name='customtier',
            name='large_thumb_size',
            field=models.IntegerField(blank=True, default=400),
        ),
        migrations.AddField(
            model_name='customtier',
            name='small_thumb_size',
            field=models.IntegerField(blank=True, default=200),
        ),
    ]
