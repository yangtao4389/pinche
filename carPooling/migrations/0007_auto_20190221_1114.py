# Generated by Django 2.0.4 on 2019-02-21 11:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carPooling', '0006_auto_20190221_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carpoolinguserconf',
            name='c_name',
            field=models.CharField(max_length=128, null=True, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='carpoolinguserconf',
            name='c_phone',
            field=models.CharField(max_length=11, null=True, verbose_name='电话号码'),
        ),
        migrations.AlterField(
            model_name='carpoolinguserconf',
            name='i_cumulative_sum',
            field=models.SmallIntegerField(default=10, null=True, verbose_name='累积积分'),
        ),
    ]