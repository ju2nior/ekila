# Generated by Django 5.1.6 on 2025-07-22 15:06

import evenslide.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evenslide', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='action',
            name='id',
            field=models.CharField(db_index=True, default=evenslide.models.ulid, editable=False, max_length=30, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='typeevenement',
            name='id',
            field=models.CharField(db_index=True, default=evenslide.models.ulid, editable=False, max_length=30, primary_key=True, serialize=False),
        ),
    ]
