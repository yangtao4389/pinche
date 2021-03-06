# Generated by Django 2.0.4 on 2019-02-27 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EventNoticeSmsSendStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(db_index=True, max_length=11, verbose_name='电话')),
                ('return_code', models.CharField(max_length=5, null=True, verbose_name='返回code')),
                ('order_id', models.CharField(help_text='如果发送成功则有订单id返回', max_length=32, null=True, verbose_name='订单')),
                ('create_time', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
            ],
            options={
                'verbose_name_plural': '验证码发送状态统计',
                'db_table': 'eventnotice_smssend_statistic',
            },
        ),
    ]
