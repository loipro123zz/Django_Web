# Generated by Django 5.0.4 on 2024-05-26 13:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0017_alter_diachigiaohang_gio_hang'),
    ]

    operations = [
        migrations.AlterField(
            model_name='diachigiaohang',
            name='gio_hang',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.giohang'),
        ),
    ]
