# Generated by Django 5.0.4 on 2024-05-24 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_sanpham_kich_thuoc_mucgiohang_kich_thuoc'),
    ]

    operations = [
        migrations.AddField(
            model_name='diachigiaohang',
            name='phuong',
            field=models.CharField(max_length=300, null=True),
        ),
    ]
