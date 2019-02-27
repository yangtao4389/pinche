# Generated by Django 2.0.4 on 2019-02-26 14:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('carPooling', '0013_auto_20190226_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='carpoolinguserconf',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, db_index=True, default=django.utils.timezone.now, verbose_name='创建时间'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='carpoolinguserconf',
            name='update_time',
            field=models.DateTimeField(auto_now=True, db_index=True, verbose_name='更新时间'),
        ),
    ]