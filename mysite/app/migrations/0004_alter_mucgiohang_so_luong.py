# Generated by Django 5.0.4 on 2024-05-18 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_donhang_giohang_rename_mucdonhang_mucgiohang_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mucgiohang',
            name='so_luong',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
