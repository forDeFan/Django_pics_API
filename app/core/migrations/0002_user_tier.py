# Generated by Django 3.2.6 on 2023-02-15 17:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20230215_1719'),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tier',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.DO_NOTHING, to='images.tier'),
        ),
    ]
