# Generated by Django 5.0.4 on 2024-05-26 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_alter_profile_ngay_sinh'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='ngay_sinh',
            field=models.DateField(blank=True, null=True),
        ),
    ]