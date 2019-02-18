from django.db import models

# Create your models here.
class CarPoolingCityGroup(models.Model):
    '''
    位置表
    '''


    c_key = models.CharField("关键字", max_length=128, null=False, blank=False, default='', help_text="位置键值(英文)")
    c_name = models.CharField("位置名称", max_length=128, null=False, blank=False, default='', help_text="位置名称(中文)")
    status = models.CharField("是否有效", max_length=2, choices=STATUS, null=False, blank=False, default=STATUS_T)

    class Meta:
        db_table = "hall_location"
        verbose_name_plural = "大厅首页位置表"


    def __str__(self):
        return self.c_name