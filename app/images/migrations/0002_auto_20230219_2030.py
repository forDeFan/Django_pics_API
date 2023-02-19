# Generated by Django 3.2.6 on 2023-02-19 20:30

import core.helpers
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BasicTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('thumbnail_small_size', models.IntegerField(blank=True, default=200, editable=False)),
                ('thumbnail_large_size', models.IntegerField(blank=True, default=400, editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.DeleteModel(
            name='Tier',
        ),
        migrations.RemoveField(
            model_name='image',
            name='name',
        ),
        migrations.AddField(
            model_name='image',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='image',
            name='seconds',
            field=models.IntegerField(default=300, validators=[core.helpers.validate_number_range]),
        ),
        migrations.AlterField(
            model_name='image',
            name='image_link',
            field=models.ImageField(upload_to=core.helpers.user_dir_path, validators=[django.core.validators.FileExtensionValidator(['jpg', 'png'])]),
        ),
        migrations.CreateModel(
            name='CustomTier',
            fields=[
                ('basictier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='images.basictier')),
                ('image_link', models.BooleanField(default=True)),
                ('expiring_link', models.BooleanField(default=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('images.basictier',),
        ),
        migrations.CreateModel(
            name='PremiumTier',
            fields=[
                ('basictier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='images.basictier')),
                ('image_link', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('images.basictier',),
        ),
        migrations.CreateModel(
            name='EnterpriseTier',
            fields=[
                ('premiumtier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='images.premiumtier')),
                ('expiring_link', models.BooleanField(default=True, editable=False)),
            ],
            options={
                'abstract': False,
            },
            bases=('images.premiumtier',),
        ),
    ]
