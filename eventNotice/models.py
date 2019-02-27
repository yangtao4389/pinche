from django.db import models

# Create your models here.


class EventNoticeSmsSendStatistic(models.Model):
    phone = models.CharField("电话", max_length=11, null=False, blank=False, db_index=True)
    return_code = models.CharField("返回code", max_length=5, null=True, blank=False)
    order_id = models.CharField("订单", max_length=32, null=True, blank=False,help_text="如果发送成功则有订单id返回")
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_index=True, null=False)

    class Meta:
        db_table = "eventnotice_smssend_statistic"
        verbose_name_plural = "验证码发送状态统计"