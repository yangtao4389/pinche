import json
import requests
import traceback
from datetime import datetime,timedelta
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from common import client,uuid_maker,checkparam
from common.json_result import RtnDefault,RtnCode
from carPooling.models import CarPoolingAssDetail,CarPoolingUserConf,CarPoolingCity,CarPoolingRecDetail,CurTripStatus,CarPoolingRecUnbook
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db import DatabaseError, transaction
from carPooling.globalApi import commonGetCurTripTip
from carPooling.globalSession import WOPENID
from carPooling import settings as csettings
from logging import getLogger
logger = getLogger("default")


def SaveBook(request):
    '''
    乘客订座接口
    :param request:
    :return:
    '''
    if request.method == "POST":
        userid = request.session[WOPENID]

        # 不需要判断当前行程的
        # dataresult = commonGetCurTripTip(userid)
        # if dataresult.get("result") == 0:
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该行程已经存在"), content_type="application/json")

        try:
            userObj = CarPoolingUserConf.objects.get(w_openid=userid)
            # 同时这里也可以来判断，该用户是否应该付费等情况
        except:
            logger.exception("预定接口：用户账户有问题")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "用户账户有问题"), content_type="application/json")


        assId = request.POST.get("assId")
        bookSeat = request.POST.get("bookSeat")
        startPlace= request.POST.get("startPlace")
        # phone= request.POST.get("phone")
        # saving= request.POST.get("saving")
        # agreeStatus= request.POST.get("agreeStatus")




        # 车主行程表改变
        try:
            assDetailObj = CarPoolingAssDetail.objects.get(c_id=assId)
            i_booked_seat = assDetailObj.i_booked_seat
            i_booked_seat += int(bookSeat)
            if i_booked_seat>assDetailObj.i_seat:
                return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该座位已被预定"), content_type="application/json")
            assDetailObj.i_booked_seat = i_booked_seat
        except:
            logger.exception("预定接口：该行程已撤销")
            return  HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "啊哦，该行程已撤销"), content_type="application/json")


        #  乘客行程表改变
        recDetailObj = CarPoolingRecDetail(
            c_id = uuid_maker.get_uuid_random(),
            c_userid = userid,
            c_assid = assId,
            c_username = userObj.c_name,
            c_card_owner = assDetailObj.c_card_owner,
            c_start_city = assDetailObj.c_start_city,
            c_end_city = assDetailObj.c_end_city,
            d_go_time = assDetailObj.d_go_time,
            t_remark = startPlace,
            i_booked_seat = bookSeat,
            i_status = CurTripStatus.Ing,
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
            logger.exception("预定接口：预定异常")
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "预定异常"), content_type="application/json")
        data = dict(
            detail_id = recDetailObj.c_id
        )
        print(data)
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "预定成功",data), content_type="application/json")



def GetList(request):
    '''
    获取我是乘客信息
    :param request:
    :return:
    '''
    if request.method == "POST":
        # 每页数据
        numPerPage = request.POST.get("numPerPage", 20)
        # if not checkparam.isVaildInt(numPerPage):
        #     return
        numPerPage = abs(int(numPerPage))

        # 当前查询页
        pageNum = request.POST.get("pageNum", 1)
        # if not checkparam.isVaildInt(pageNum):
        #     return
        pageNum = int(pageNum)

        allMyAss = CarPoolingRecDetail.objects.filter(status=True).filter(c_userid=request.session[WOPENID]).order_by("-d_go_time")
        paginator = Paginator(allMyAss, numPerPage)
        page = paginator.page(pageNum)

        # "CurrentPageIndex": 1, "PageSize": 20, "RowCount": 66, "PageCount": 4, "IsFirstPage": true, "IsLastPage": false, "CurrentRowCount": 20, "CurrentStartIndex": 1, "CurrentEndIndex": 20
        resultDict = dict(
            CurrentPageIndex=pageNum,
            PageSize=numPerPage,
            RowCount=paginator.count,
            PageCount=paginator.num_pages,
            IsFirstPage=not page.has_previous(),
            IsLastPage=not page.has_next(),
            CurrentRowCount=page.__len__(),
            CurrentStartIndex=1 if page.__len__() >= 1 else 0,
            CurrentEndIndex=page.__len__(),

        )
        DataSource = []
        for i in page.object_list:
            dictItem = dict(
                Id=i.c_id,
                StartCity = i.c_start_city,
                EndCity = i.c_end_city,
                GoTime=i.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                CarOwner=i.c_card_owner,
                UserId=i.c_userid,
                # BusType=i.c_bus_type,
                # Line=i.t_line,
                # Seat=i.i_no_booked_seat,  # 余座BookSeat
                BookSeat=i.i_booked_seat, # 定座
                StartPlace=i.t_remark, # 定座
                Status = i.i_status,

            )
            DataSource.append(dictItem)
        resultDict.update(DataSource=DataSource)

        # assList = {"DataSource":[
        #     {"Id":"930302a5-565e-462b-84c4-abcd10922796","GoTime":"2019/2/20 9:00:00","CardOwner":"周正","UserId":"758038ca-84dc-4073-ace7-2616952db52b","BusType":"福特福睿斯。","Line":"温江出发，到达达州南外。","Cash":120.00,"Remark":"顺路上下，支持群价，预订后请电话确认一下。--点击“预订”即可，李。","Seat":2,"GoodNum":0,"BadNum":0,"IsRealName":0,"IsRealDriver":0}],
        #         "CurrentPageIndex":1,
        #         "PageSize":20,
        #         "RowCount":1,
        #         "PageCount":1,
        #         "IsFirstPage":"true",
        #         "IsLastPage":"true",
        #         "CurrentRowCount":1,
        #         "CurrentStartIndex":1,
        #         "CurrentEndIndex":1,
        # }
        print(resultDict)
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok",resultDict), content_type="application/json")

def GetDetailData(request):
    if request.method == "POST":
        id = request.POST.get("id")
        if not id:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "no params"), content_type="application/json")
        try:
            # 去数据库查看当前Id是否存在
            recObj = CarPoolingRecDetail.objects.get(c_id=id,status=True)
            assObj = CarPoolingAssDetail.objects.get(c_id=recObj.c_assid)
            assUserObj = CarPoolingUserConf.objects.get(w_openid=assObj.c_userid)
            dataDict = dict(
                Id=id,  # 乘客行程id
                AssId = recObj.c_assid,  # 车主发布的详情
                StartCity=recObj.c_start_city,
                EndCity=recObj.c_end_city,
                GoTime=recObj.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                BookedSeat=recObj.i_booked_seat,  # 预定了的座位
                Remark=recObj.t_remark,
                CarOwner=recObj.c_card_owner,
                Status=recObj.i_status,
                # UserId=assObj.c_userid,

                BusType = assObj.c_bus_type,

                Phone = assUserObj.c_phone,

            )
            print(dataDict)
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok", dataDict), content_type="application/json")
        except:
            print(traceback.print_exc())
            # 没有数据
            dataDict = dict(
                Id=id,
                UserId=request.session[WOPENID],
                Status=1,
                # GoTime = datetime.strftime(datetime.now() + timedelta(minutes=10),"%Y-%m-%d %H:%M:%S")
            )
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该id不存在", dataDict), content_type="application/json")


def Del(request):
    '''删除用户行程记录'''
    if request.method == "POST":
        id = request.POST.get("id")
        try:
            assObj = CarPoolingRecDetail.objects.get(c_id=id)
            if assObj.i_status == 1 or assObj.i_status == 2:
                return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "只有已完成的行程才可以删除"), content_type="application/json")
            assObj.status = False
            assObj.save()
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "删除成功"), content_type="application/json")
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "删除失败，联系管理员"), content_type="application/json")

def UnbookSave(request):
    if request.method == "POST":
        RecId = request.POST.get("RecId")
        unsubscribeTags = request.POST.get("unsubscribeTags")
        unsubscribeComplain = request.POST.get("unsubscribeComplain")
        # 退订  乘客行程动态改变，车主行程动态改变，通知

        recObjList = CarPoolingRecDetail.objects.filter(c_id=RecId).filter(status=True).filter(i_status=CurTripStatus.Ing)
        if len(recObjList) != 1:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "退订失败，该行程已删除|取消|出发|完成"), content_type="application/json")
        recObj = recObjList[0]
        assObjList = CarPoolingAssDetail.objects.filter(c_id=recObj.c_assid)
        if len(assObjList) != 1:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "退订失败，系统错误"),
                                content_type="application/json")
        assObj = assObjList[0]

        try:
            recObj.i_status = CurTripStatus.Cancel
            assObj.i_booked_seat -= recObj.i_booked_seat
            recUnbookObj,created = CarPoolingRecUnbook.objects.get_or_create(c_recid=recObj.c_id)
            recUnbookObj.unsubscribeTags = unsubscribeTags
            recUnbookObj.unsubscribeComplain = unsubscribeComplain
            with transaction.atomic():  # 事务，保证唯一 存在，则都存在。错误，则都不去改变
                recObj.save()
                assObj.save()
                recUnbookObj.save()
            #todo 这里需要通知
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "退订成功"),
                                content_type="application/json")
        except:
            print(traceback.print_exc())
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "退订失败，请稍后重试"),
                                content_type="application/json")