import json
import requests
import traceback
from datetime import datetime,timedelta
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from common import client,uuid_maker,checkparam
from common.json_result import RtnDefault,RtnCode
from carPooling.models import CarPoolingAssDetail,CarPoolingUserConf,CarPoolingCity,CarPoolingRecDetail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import DatabaseError, transaction

from logging import getLogger
logger = getLogger("default")


def SaveBook(request):
    '''
    乘客订座接口
    :param request:
    :return:
    '''
    if request.method == "POST":
        assId = request.POST.get("assId")
        bookSeat = request.POST.get("bookSeat")
        startPlace= request.POST.get("startPlace")
        phone= request.POST.get("phone")
        saving= request.POST.get("saving")
        agreeStatus= request.POST.get("agreeStatus")

        # 是否已经存在该行程，如果存在，则直接跳转到行程详情页
        # try:
        #     CarPoolingRecDetail.objects.get(c_userid = request.session["c_weixin_id"],c_assid = assId)
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "已经预定过"), content_type="application/json")
        # except:
        #     pass


        # 车主行程表改变
        assDetailObj = CarPoolingAssDetail.objects.get(c_id=assId)
        i_booked_seat = assDetailObj.i_booked_seat
        i_booked_seat += int(bookSeat)
        if i_booked_seat>assDetailObj.i_seat:
            return
        assDetailObj.i_booked_seat = i_booked_seat

        #  乘客行程表改变
        recDetailObj = CarPoolingRecDetail(
            c_id = uuid_maker.get_uuid_random(),
            c_userid = request.session["c_weixin_id"],
            c_assid = assId,
            t_remark = startPlace,
            i_booked_seat = bookSeat,
            c_phone = phone,
            i_status = 1,
            status = True,
        )

        try:
            with transaction.atomic():  # 事务，保证唯一 存在，则都存在。错误，则都不去改变
                assDetailObj.save()
                recDetailObj.save()
        # except DatabaseError:
        #     print(traceback.print_exc())
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "预定异常"), content_type="application/json")
        except:
            print(traceback.print_exc())
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "预定异常"), content_type="application/json")
        data = dict(
            detail_id = recDetailObj.c_id
        )
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "预定成功",data), content_type="application/json")



def GetList(request):
    pass

def GetDetailData(request):
    pass

