# Generated by Django 5.0.4 on 2024-05-26 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_alter_profile_hinh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ho_ten',
            field=models.CharField(blank=True, default='', max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sdt',
            field=models.CharField(blank=True, default='', max_length=20, null=True),
        ),
    ]