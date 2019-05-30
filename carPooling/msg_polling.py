# import sys
# import os
# #  获取当前文件的路径，以及路径的父级文件夹名
# pwd = os.path.dirname(os.path.realpath(__file__))
# # print(pwd)
# # 将项目目录加入setting
# sys.path.append(pwd + "../")
# print(sys.path)
# # sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
# # manage.py中
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_app.settings")
# # os.environ.update("DJANGO_SETTINGS_MODULE", "django_app.settings")
# # a = 1/0
# import django
# django.setup()
#  消息轮询。主要在程序跑起来的时候，开一个进程去执行？？
import time,os
from datetime import datetime,timedelta
from threading import Thread
from copy import deepcopy

from django.core.cache import cache
from django.db import DatabaseError, transaction
from django.shortcuts import HttpResponse

from app_weixin.settings import template_id_004,logger,template_id_005

from carPooling import settings as csettings
from carPooling.models import CarPoolingAssDetail,CurTripStatus,CarPoolingUserConf,CarPoolingRecDetail
from carPooling.tasks import aync_wx_template


def runserver_from_start(request):
    '''
    django 不支持一直启动该程序，所以只能用定时器来启动了。
    :return:
    '''
    POLLING_TIME = 2  # 轮询时间2分钟
    #4小时前的时间


    # while True:
    logger.info("轮询开始")
    cache.get("msg_polling_now",datetime.now())
    # now = datetime.now()
    now = datetime(2019, 5, 30, 11, 10, 31, 840000)
    now_less_minutes = now-timedelta(minutes=POLLING_TIME)
    # 任务一  行程出发提醒
    #                                                                        时间                                          状态                                  位数
    ass_detail_list = CarPoolingAssDetail.objects.filter(status=True).filter(d_go_time__range =(now_less_minutes,now)).filter(i_status=CurTripStatus.Ing)
    trip_start_msg(ass_detail_list)
    # t1 = Thread(target=trip_start_msg,args=(deepcopy(ass_detail_list),))
    logger.info("行程出发提醒车主数量：%s"%len(ass_detail_list))


    # 任务二 行程结束提醒
    last = now-timedelta(hours=4)
    last_less_minutes = last-timedelta(minutes=POLLING_TIME)
    ass_detail_list_o = CarPoolingAssDetail.objects.filter(status=True).filter(d_go_time__range =(last_less_minutes,last)).filter(i_status=CurTripStatus.Gone)
    trip_end_msg(ass_detail_list_o)
    logger.info("行程结束提醒车主数量：%s" % len(ass_detail_list_o))
    logger.info("轮询结束")
    return HttpResponse("OK")

# 任务一
def trip_start_msg(ass_detail_list):
    logger.info("任务一")
    for i in ass_detail_list:
        logger.info("遍历车主行程")


        # 发送信息
        template_data = dict(
            first=dict(value="您好，您有行程即将开始。", color="#173177"),
            keyword1=dict(value=i.c_id, color="#173177"),
            keyword2=dict(value=i.d_go_time, color="#173177"),
            keyword3=dict(value="%s->%s"%(i.c_start_city,i.c_end_city), color="#173177"),
            # keyword4=dict(value=i.i_booked_seat, color="#173177"),
            # keyword5=dict(value=ass_obj_phone, color="#173177"),
            remark=dict(value="查看乘客信息请点击详情", color="#173177"),
        )
        template_url = csettings.DEFAULT_UserAssDetail_FULL_PATH % i.c_id
        if os.name != "posix":
            if i.i_booked_seat >= 1:
                aync_wx_template(template_id_004, i.c_userid, template_data, template_url)
        else:
            if i.i_booked_seat >= 1:
                aync_wx_template.delay(template_id_004, i.c_userid, template_data, template_url)

        rec_detail_list = CarPoolingRecDetail.objects.filter(c_assid=i.c_id).filter(i_status=CurTripStatus.Ing)
        for j in rec_detail_list:
            logger.info("遍历乘客行程")
            template_data = dict(
                first=dict(value="您好，您有行程即将开始。", color="#173177"),
                keyword1=dict(value=j.c_id, color="#173177"),
                keyword2=dict(value=i.d_go_time, color="#173177"),
                keyword3=dict(value="%s->%s" % (i.c_start_city, i.c_end_city), color="#173177"),
                # keyword4=dict(value=j.i_booked_seat, color="#173177"),
                # keyword5=dict(value=ass_obj_phone, color="#173177"),
                remark=dict(value="查看车主信息请点击详情", color="#173177"),
            )
            template_url = csettings.DEFAULT_UserRecDetail_FULL_PATH % j.c_id
            if os.name != "posix":
                aync_wx_template(template_id_004, j.c_userid, template_data, template_url)
            else:
                aync_wx_template.delay(template_id_004, j.c_userid, template_data, template_url)

        try:
            with transaction.atomic():  # 事务，保证唯一 存在，则都存在。错误，则都不去改变
                i.i_status = CurTripStatus.Gone
                i.save()
                rec_detail_list.update(i_status=CurTripStatus.Gone)

        except:
            logger.exception("开始通知异常")


# 任务二  结束通知
def trip_end_msg(ass_detail_list):
    logger.info("任务二  结束通知")
    for i in ass_detail_list:
        logger.info("遍历车主行程")
        # 发送信息
        template_data = dict(
            first=dict(value="您好，您的行程已经结束", color="#173177"),
            keyword1=dict(value=i.c_card_owner, color="#173177"),
            keyword2=dict(value=i.c_bus_type, color="#173177"),
            # keyword3=dict(value="%s->%s" % (i.c_start_city, i.c_end_city), color="#173177"),
            # keyword4=dict(value=i.i_booked_seat, color="#173177"),
            # keyword5=dict(value=ass_obj_phone, color="#173177"),
            remark=dict(value="感谢使用里行", color="#173177"),
        )
        template_url = csettings.DEFAULT_UserAssDetail_FULL_PATH % i.c_id
        if os.name != "posix":
            if i.i_booked_seat >= 1:
                aync_wx_template(template_id_005, i.c_userid, template_data, template_url)
        else:
            if i.i_booked_seat >= 1:
                aync_wx_template.delay(template_id_005, i.c_userid, template_data, template_url)

        rec_detail_list = CarPoolingRecDetail.objects.filter(c_assid=i.c_id).filter(i_status=CurTripStatus.Gone)
        for j in rec_detail_list:
            logger.info("遍历乘客行程")
            template_data = dict(
                first=dict(value="您好，您有行程已经结束", color="#173177"),
                keyword1=dict(value=i.c_card_owner, color="#173177"),
                keyword2=dict(value=i.c_bus_type, color="#173177"),

                remark=dict(value="感谢使用里行", color="#173177"),
            )
            template_url = csettings.DEFAULT_UserRecDetail_FULL_PATH % j.c_id
            if os.name != "posix":
                aync_wx_template(template_id_005, j.c_userid, template_data, template_url)
            else:
                aync_wx_template.delay(template_id_005, j.c_userid, template_data, template_url)

        try:
            with transaction.atomic():  # 事务，保证唯一 存在，则都存在。错误，则都不去改变
                i.i_status = CurTripStatus.Done
                i.save()
                rec_detail_list.update(i_status=CurTripStatus.Done)

        except:
            logger.exception("开始通知异常")