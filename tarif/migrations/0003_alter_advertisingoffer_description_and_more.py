# Generated by Django 5.1.6 on 2025-07-24 11:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tarif', '0002_alter_advertisingoffer_description_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='advertisingoffer',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='offercategory',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
        migrations.AlterField(
            model_name='order',
            name='description',
            field=ckeditor.fields.RichTextField(blank=True, verbose_name='Description'),
        ),
    ]
