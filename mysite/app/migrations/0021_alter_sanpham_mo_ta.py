# Generated by Django 5.0.4 on 2024-05-26 15:29

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0020_alter_sanpham_mo_ta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sanpham',
            name='mo_ta',
            field=ckeditor.fields.RichTextField(blank=True, default=''),
        ),
    ]