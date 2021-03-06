from django.db import models
from xpinyin import Pinyin
# Create your models here.
class CurTripStatus():
    '''
    当前行程状态
    '''
    Cancel = 0  # 取消
    Ing = 1 # 行程进行中
    Gone = 2 # 行程已出发
    Done = 3 # 完成

class StatusTrueManager(models.Manager):
    '''
    #首先,定义一个Manager的子类 如果使用，会覆盖默认的objects
    '''
    def get_queryset(self):
        return super(StatusTrueManager, self).get_queryset().filter(status=True)


class CarPoolingAssDetail(models.Model):
    '''
    行程表
    '''
    c_id = models.CharField("行程唯一id", max_length=128, null=False, blank=False, unique=True,db_index=True)
    c_userid = models.CharField("车主id", max_length=128, null=False, blank=False, db_index=True)
    c_card_owner = models.CharField("车主姓名", max_length=128, null=True, blank=False,)
    # c_user_phone = models.CharField("车主电话" ,max_length=11, null=True, blank=False, )
    c_start_city = models.CharField("出发城市", max_length=128, null=False, blank=False,db_index=True)
    c_end_city =  models.CharField("到达城市", max_length=128, null=False, blank=False,db_index=True)
    t_line = models.TextField("路线",null=True, blank=False, default='')
    d_go_time = models.DateTimeField("出发时间",null=False, blank=False, db_index=True)
    c_bus_type = models.CharField("车型", max_length=128, null=True, blank=False)
    i_vehicle_number = models.SmallIntegerField("该车型荷载", null=True, blank=True)
    i_seat = models.SmallIntegerField("总共座位",null=False, blank=True, default=0)
    i_booked_seat = models.SmallIntegerField("已预订的座位", null=False, blank=False, default=0)
    i_no_booked_seat = models.SmallIntegerField("剩余座位", null=False, blank=False,db_index=True)
    i_cash = models.IntegerField("费用", null=False, blank=False, default=0)
    t_remark = models.TextField("备注",  null=True, blank=False, default='')
    i_status = models.SmallIntegerField("行程状态",null=False,help_text=("参考CurTripStatus"))
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, db_index=True, null=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_index=True, null=False)
    status = models.BooleanField("是否删除", null=False, blank=False, default=True, help_text="true,false,用于用户显示")

    class Meta:
        db_table = "carpooling_ass_detail"
        verbose_name_plural = "行程表(中心表)"


    # def __str__(self):
    #     return self.c_name

    def save(self, *args, **kwargs):
        self.i_no_booked_seat = self.i_seat - self.i_booked_seat
        if self.i_no_booked_seat<0:
            raise Exception("i_no_booked_seat is not fushu")
        super(CarPoolingAssDetail, self).save()

    @property
    def list_field(self):
        return ['c_id', 'c_userid', 'c_card_owner', 'status']

class CarPoolingUserConf(models.Model):
    '''
    用户表
    以w_开头的都是来源于微信的数据
    可以通过微信id跟电话来查到对应的用户。微信id不能为空，电话可以
    '''
    # c_userid = models.CharField("用户id", max_length=128, null=False, blank=False, db_index=True,unique=True )


    w_openid = models.CharField("微信id", max_length=128, null=False, blank=False,db_index=True,help_text="微信用户的唯一标识")
    w_nickname =  models.CharField("用户昵称", max_length=128, null=True, blank=False)
    w_sex = models.SmallIntegerField("用户的性别",null=True, blank=False,help_text="值为1时是男性，值为2时是女性，值为0时是未知")
    w_country = models.CharField("国家", max_length=128, null=True, blank=False)
    w_province = models.CharField("省份", max_length=128, null=True, blank=False)
    w_city = models.CharField("城市", max_length=128, null=True, blank=False)
    w_headimgurl = models.CharField("用户头像", max_length=256, null=True, blank=False,help_text="用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。")

    c_name = models.CharField("真实姓名", max_length=128, null=True, blank=False,)
    c_phone = models.CharField("电话号码" ,max_length=11, null=True, blank=False,db_index=True)
    b_phone_status = models.BooleanField("电话号码状态" , null=False, blank=False, default=False,help_text="true,false")
    i_cumulative_sum = models.SmallIntegerField("累积积分" , null=True, blank=False, default=10)
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, db_index=True, null=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_index=True, null=False)
    status = models.BooleanField("是否有效" , null=False, blank=False, default=True,help_text="true,false")

    class Meta:
        db_table = "carpooling_user_conf"
        verbose_name_plural = "用户表"


    def __str__(self):
        return self.w_nickname

    @property
    def list_field(self):
        return ['w_nickname', 'c_name', 'status']



class CarPoolingCity(models.Model):
    '''
    城市表
    '''
    c_fullname = models.CharField("城市名", max_length=128, null=False, blank=False,db_index=True,unique=True )
    c_firstname = models.CharField("首字母(大写)", max_length=10,null=False,blank=False,db_index=True,editable=False)
    status = models.BooleanField("是否有效", null=False, blank=False, default=True, help_text="true,false")

    # objects_status_true = StatusTrueManager()

    class Meta:
        db_table = "carpooling_city"
        verbose_name_plural = "城市列表"

    def save(self, *args, **kwargs):
        p = Pinyin()
        self.c_firstname = p.get_initials(self.c_fullname,"").upper()[0]
        super(CarPoolingCity, self).save()

    @classmethod
    def get_status_true(cls):
        return cls.objects.filter(status=True).order_by("c_firstname")

    @classmethod
    def get_all_city(cls):
        '''
        :return: 所有城市
        '''
        return cls.get_status_true().all().order_by("c_firstname")

    # @classmethod
    # def get_all_groups(cls):
    #     '''
    #     :return: 所有城市
    #     '''
    #     return cls.get_status_true().annotate(models.Count('c_firstname')).order_by("c_firstname")


    def __str__(self):
        return self.c_fullname

    @property
    def list_field(self):
        return ['c_fullname', 'c_firstname', 'status']



class CarPoolingRecDetail(models.Model):
    '''
    乘客与行程关联表，暂时用非关联表，直接存放必要字段即可。
    '''
    c_id = models.CharField("行程唯一id", max_length=128, null=False, blank=False, unique=True, db_index=True)
    c_userid = models.CharField("乘客id", max_length=128, null=False, blank=False, db_index=True)
    c_assid = models.CharField("行程id", max_length=128, null=False, blank=False, db_index=True)
    c_username = models.CharField("乘客姓名", max_length=128, null=False, blank=False, )
    c_card_owner = models.CharField("车主姓名", max_length=128, null=False, blank=False, )
    # c_user_phone = models.CharField("车主电话", max_length=11, null=False, blank=False, )
    c_start_city = models.CharField("出发城市", max_length=128, null=False, blank=False, db_index=True)
    c_end_city = models.CharField("到达城市", max_length=128, null=False, blank=False, db_index=True)
    d_go_time = models.DateTimeField("出发时间", null=True, blank=False, db_index=True)
    t_remark = models.TextField("备注", null=True, blank=False, default='')
    i_booked_seat = models.SmallIntegerField("预定座位数", null=False, blank=True)
    # c_phone = models.CharField("电话号码", max_length=11, null=True, blank=False, )
    i_status = models.SmallIntegerField("行程状态",null=False,help_text=("参考CurTripStatus"))
    update_time = models.DateTimeField(verbose_name="更新时间", auto_now=True, db_index=True, null=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True, db_index=True, null=False)
    status = models.BooleanField("是否删除", null=False, blank=False, default=True, help_text="true,false,用于用户显示")

    class Meta:
        db_table = "carpooling_rec_detail"
        verbose_name_plural = "乘客行程关联表"
        unique_together = ["c_assid","c_userid"]  # 一个用户最多关联一次该行程


class CarPoolingRecUnbook(models.Model):
    c_recid = models.CharField("乘客行程id", max_length=128, null=False, blank=False, unique=True, db_index=True)
    unsubscribeTags = models.CharField("乘客取消原因", max_length=128, null=True, blank=False, )
    unsubscribeComplain = models.CharField("投诉原因", max_length=128, null=True, blank=False, )

    class Meta:
        db_table = "carpooling_rec_unbook"
        verbose_name_plural = "乘客退订详情统计表"