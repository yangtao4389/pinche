import json
import requests
import traceback
from datetime import datetime,timedelta
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from common import client,uuid_maker,checkparam
from common.json_result import RtnDefault,RtnCode
from carPooling.models import CarPoolingAssDetail,CarPoolingUserConf,CarPoolingCity,CurTripStatus,CarPoolingRecDetail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from carPooling.globalApi import commonGetCurTripTip
from django.db import DatabaseError, transaction
from logging import getLogger
logger = getLogger("default")


# Create your views here.
def GetDetailData(request):
    '''
    原文是post请求
    :param request:
    :return:
    '''
    if request.method == "POST":
        id = request.POST.get("id")
        if not id:
            return HttpResponse("no id")

        try:
            # 去数据库查看当前Id是否存在
            assObj = CarPoolingAssDetail.objects.get(c_id=id)
            dataDict = dict(
                Id=id,
                StartCity = assObj.c_start_city,
                EndCity = assObj.c_end_city,
                Line = assObj.t_line,
                GoTime=assObj.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                BusType=assObj.c_bus_type,
                VehicleNumber=assObj.i_vehicle_number,
                Seat=assObj.i_seat , # 总共座位
                BookedSeat=assObj.i_booked_seat, # 预定了的座位
                Cash=assObj.i_cash,
                Remark=assObj.t_remark,
                CardOwner=assObj.c_card_owner,
                Status=assObj.i_status,
                UserId=assObj.c_userid,
                NoBookedSeat=assObj.i_no_booked_seat,


            )

            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "已下过单用户",dataDict), content_type="application/json")
        except:
            print(traceback.print_exc())
            dataDict = dict(
                Id = id,
                UserId = request.session["w_openid"],
                Status= 1,
                # GoTime = datetime.strftime(datetime.now() + timedelta(minutes=10),"%Y-%m-%d %H:%M:%S")
            )
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK,"该id不存在",dataDict), content_type="application/json")
        # # print(Id)
        # if not Id:
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM,"没有id"), content_type="application/json")
        # data = '''
        #  {"statusCode":200,"message":"操作成功!","data":{"Id":"b8cf77a3-c671-4560-9bed-a746b8a52276","StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","GoTime":"2019/2/20 0:00:00","BusType":"丰田致炫","VehicleNumber":null,"Seat":3,"BookedSeat":0,"Cash":100.00,
        # "Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","Status":1,"UserId":"4177159e-898c-4cc5-91ac-cc38c62e3c10"}}
        # '''
        # 如果有记录，返回最后一条。如果没有，data直接返回
        # data = {
        #     "Status": 1,  # 0代表提交成功，但未正常实现。1代表可以编辑，2代表行程结束
        # }
        # return HttpResponse(RtnDefault(RtnCode.STATUS_OK,"新用户",data), content_type="application/json")


def GetRecListByAss(request):
    '''
    车主 根据assid来获取所有乘客信息
    :return:
    '''
    if request.method == "POST":
        assid = request.POST.get("assid")
        reclist = CarPoolingRecDetail.objects.filter(c_assid=assid).exclude(i_status=CurTripStatus.Cancel).all()
        newRecList = []
        for obj in reclist:
            dictItem = dict(
                Id = obj.c_userid,
                Name=obj.c_username,
                Phone=CarPoolingUserConf.objects.get(w_openid=obj.c_userid).c_phone,
                BookSeat=obj.i_booked_seat,
                StartPlace=obj.t_remark,
            )
            newRecList.append(dictItem)
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok", newRecList), content_type="application/json")



def GetLastAss(request):
    '''
    时刻去请求，可能是保存页面其它内容用
    :param request:
    :return:
    '''
    if request.method == "POST":
        dataDict = dict()
        StartCity = request.POST.get("StartCity")
        EndCity = request.POST.get("EndCity")
        # print(StartCity,EndCity)
        # 获取用户信息
        userObj = CarPoolingUserConf.objects.get(w_openid=request.session['w_openid'])
        dataDict.update(
            Phone = userObj.c_phone,
            Name = userObj.c_name,
        )

        # print(StartCity,EndCity)
        # 如果有这条线路的，则返回已经填过的信息，如果没有，只保留车的信息，其余都改变
        assDetailQuery = CarPoolingAssDetail.objects.filter(c_userid=request.session['w_openid'])

        if len(assDetailQuery) > 0:
            # 已在系统中存在过，则bus信息可以保留
            dataDict.update(
                Seat=assDetailQuery[0].i_seat,
                BusType=assDetailQuery[0].c_bus_type,
                Cash=assDetailQuery[0].i_cash,
            )
            detailGoAndEndCity = assDetailQuery.filter(c_start_city=StartCity, c_end_city=EndCity)
            if len(detailGoAndEndCity) > 0:
                assObj = detailGoAndEndCity[0]
                dataDict.update(
                    StartCity=assObj.c_start_city,
                    EndCity=assObj.c_end_city,
                    Line=assObj.t_line,
                    Seat=assObj.i_seat,
                    Cash=assObj.i_cash,
                    Remark=assObj.t_remark,
                    # Phone=assObj.c_user_phone,
                    CardOwner=assObj.c_card_owner,
                    BusType=assObj.c_bus_type,
                    VehicleNumber=assObj.i_vehicle_number,
                )


        # 如果没找到，
        if StartCity != "undefined" and EndCity != "undefined":  # 都存在
            dictItem = {"StartCity": StartCity, "EndCity": EndCity}
        elif StartCity != "undefined" and EndCity == "undefined":
            dictItem = {"StartCity": StartCity, "EndCity": None}
        elif  StartCity == "undefined" and EndCity != "undefined" :
            dictItem = {"StartCity": None, "EndCity": EndCity}
        else:
            dictItem = {"StartCity": None, "EndCity": None}

        dataDict.update(dictItem)



        # Line = request.POST.get("Line")
        # Seat = request.POST.get("Seat")
        # Cash = request.POST.get("Cash")
        # Remark = request.POST.get("Remark")
        # BusType = request.POST.get("BusType")
        # VehicleNumber = request.POST.get("VehicleNumber")
        # Phone = request.POST.get("Phone")
        # CardOwner = request.POST.get("CardOwner")
        # {"StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","Seat":3,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","BusType":"丰田致炫","VehicleNumber":null}
        # {"StartCity":"广元","EndCity":"成都","Line":"XX 出发，XX 站上高速，XX 站下高速，途径X 号线XX 地铁站（推荐下车点），最终目的地：XX","Seat":3,"Cash":100,"Remark":"顺路上下，支持群价，预订后请电话确认一下。","Phone":"18649715651","CardOwner":"小杨","BusType":null,"VehicleNumber":null}
        # data = {"StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","Seat":3,
        # "Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","BusType":"丰田致炫","VehicleNumber":None}

        return HttpResponse(json.dumps(dataDict),content_type="application/json")

def Cancel(request):
    if request.method == "POST":
        Id = request.POST.get("Id")
        try:
            assDetailObj = CarPoolingAssDetail.objects.get(c_id=Id)
            if assDetailObj.status != True or assDetailObj.i_status != CurTripStatus.Ing:
                return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该行程已取消|出发|完成，修改无效"),
                                    content_type="application/json")
            assDetailObj.i_status = CurTripStatus.Cancel

            # 查看所有乘客，并取消他们的行程 #todo 这里需要通知所有用户
            recDetailObj = CarPoolingRecDetail.objects.filter(c_assid=Id).filter(i_status=CurTripStatus.Ing).filter(status=True)

            with transaction.atomic():  # 事务，保证唯一 存在，则都存在。错误，则都不去改变
                assDetailObj.save()
                recDetailObj.update(i_status=CurTripStatus.Cancel)

            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "取消行程成功"), content_type="application/json")
        except:
            print(traceback.print_exc())
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该行程不存在"), content_type="application/json")


def noLeftSeat(request):
    '''
    将车主发布的行程设置为剩余座位设置为0
    该行程必须是在进行中，未出发，未删除的行程
    :param request:
    :return:
    '''
    if request.method == "POST":
        Id = request.POST.get("Id")
        try:
            assDetailObj = CarPoolingAssDetail.objects.get(c_id=Id)
            if assDetailObj.status != True or assDetailObj.i_status != CurTripStatus.Ing:
                return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该行程已取消|出发|完成，修改无效"), content_type="application/json")
            assDetailObj.i_seat = assDetailObj.i_booked_seat
            assDetailObj.save()
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "余座设置为0成功"), content_type="application/json")
        except:
            print(traceback.print_exc())
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该行程不存在"), content_type="application/json")





def SaveEdit(request):
    '''
    一个用户在同一个时间段，只能有一条数据
    :param request:
    :return:
    '''
    if request.method == "POST":
        Id = request.POST.get("Id")
        if not Id:
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "请刷新页面重试"), content_type="application/json")

        # 验证所有参数
        StartCity = request.POST.get("StartCity")
        EndCity = request.POST.get("EndCity")
        try:
            CarPoolingCity.objects.get(c_fullname=StartCity, status=True)
            CarPoolingCity.objects.get(c_fullname=EndCity, status=True)
        except:
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发或到达城市不存在"), content_type="application/json")

        GoTime = request.POST.get("GoTime")
        if not checkparam.isVaildDateTime(GoTime):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发时间有误"), content_type="application/json")
        if GoTime > str(datetime.now()):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发时间有误"), content_type="application/json")

        # VehicleNumber = request.POST.get("VehicleNumber")
        # if VehicleNumber and not checkparam.isVaildInt(VehicleNumber):

        Seat = request.POST.get("Seat")
        if not checkparam.isVaildInt(Seat):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座出错"), content_type="application/json")
        Seat = int(Seat)
        if Seat > 6 or Seat < 1:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座数量出错"), content_type="application/json")

        Cash = request.POST.get("Cash")
        if not checkparam.isVaildInt(Cash):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "费用出错"), content_type="application/json")
        Cash = int(Cash)
        if Cash > 200 or Cash <= 0:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "设置费用出错"), content_type="application/json")


        try:

            userObj = CarPoolingUserConf.objects.get(w_openid=request.session["w_openid"])
        except:
            # 用户id不存在，直接去login页面
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponseRedirect(settings.LOGIN_URL)

        try:
            # todo 这里需要改动，只能是在未删除，且未预定的情况下才能修改。如果直接设置为0呢？？好像也可以。
            assDeatilObj = CarPoolingAssDetail.objects.filter(c_id=Id).filter(status=True).filter(
                i_status=CurTripStatus.Ing)
            if len(assDeatilObj) > 0 :
                assDeatilObj = assDeatilObj[0]
            else:
                raise Exception
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "该状态不能被编辑"), content_type="application/json")
        # todo 查看是否有乘客了。如果有，只能将剩余座位设置为0，其它的都不能变。
        recDetailList = CarPoolingRecDetail.objects.filter(c_assid=Id).filter(status=True).filter(
            i_status=CurTripStatus.Ing)
        if len(recDetailList) > 0:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "已有乘客预定，该状态不能被编辑"),
                                content_type="application/json")


        try:
            assDeatilObj.c_start_city =StartCity
            assDeatilObj.c_end_city =EndCity
            assDeatilObj.t_line = request.POST.get("Line")
            assDeatilObj.d_go_time = GoTime
            assDeatilObj.c_bus_type = request.POST.get("BusType")
            # assDeatilObj.i_vehicle_number = None
            assDeatilObj.i_seat = Seat
            # assDeatilObj.i_booked_seat = 0
            assDeatilObj.i_cash = Cash
            assDeatilObj.t_remark = request.POST.get("Remark")
            assDeatilObj.status = True
            assDeatilObj.save()
        except:
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            data = {
                "Code": 300,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
            }
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "数据存储出错，请联系客服"), content_type="application/json")

        data = {
            "Code": 200,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
        }
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "下单成功，去分享", data), content_type="application/json")


def SavePublish(request):
    '''
    一个用户在同一个时间段，只能有一条数据
    :param request:
    :return:
    '''
    if request.method == "POST":
        id = request.POST.get("id")
        if not id:
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "请刷新页面重试"), content_type="application/json")
        try:

            userObj = CarPoolingUserConf.objects.get(w_openid=request.session["w_openid"])
        except:
            # 用户id不存在，直接去login页面
            # print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "用户信息不全"), content_type="application/json")



        # 验证所有参数
        StartCity = request.POST.get("StartCity")
        EndCity = request.POST.get("EndCity")
        try:
            CarPoolingCity.objects.get(c_fullname = StartCity,status=True)
            CarPoolingCity.objects.get(c_fullname = EndCity,status=True)
        except:
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发或到达城市不存在"), content_type="application/json")


        GoTime = request.POST.get("GoTime")
        if not checkparam.isVaildDateTime(GoTime):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发时间有误"), content_type="application/json")
        if GoTime < str(datetime.now()):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "出发时间有误"), content_type="application/json")

        # VehicleNumber = request.POST.get("VehicleNumber")
        # if VehicleNumber and not checkparam.isVaildInt(VehicleNumber):

        Seat=request.POST.get("Seat")
        if not checkparam.isVaildInt(Seat):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座出错"), content_type="application/json")
        Seat = int(Seat)
        if Seat>6 or Seat<1:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座数量出错"), content_type="application/json")

        Cash = request.POST.get("Cash")
        if not checkparam.isVaildInt(Cash):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "费用出错"), content_type="application/json")
        Cash = int(Cash)
        if Cash>200 or Cash <= 0:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "设置费用出错"), content_type="application/json")



        try:
            #todo 差是否需要验证当前用户的行程状态。
            userid = userObj.w_openid
            dataresult = commonGetCurTripTip(userid)
            print(dataresult)
            if dataresult.get("result") == 0:
                return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "已经存在"), content_type="application/json")
            # assDeatilObj,created = CarPoolingAssDetail.objects.get_or_create(c_id=id)
            assDeatilObj= CarPoolingAssDetail()
            assDeatilObj.c_id = id
            assDeatilObj.c_userid = userObj.w_openid
            assDeatilObj.c_card_owner = userObj.c_name
            # assDeatilObj.c_user_phone = userObj.c_phone
            assDeatilObj.c_start_city =StartCity
            assDeatilObj.c_end_city =EndCity
            assDeatilObj.t_line = request.POST.get("Line")
            assDeatilObj.d_go_time = GoTime
            assDeatilObj.c_bus_type = request.POST.get("BusType")
            assDeatilObj.i_vehicle_number = None
            assDeatilObj.i_seat = Seat
            assDeatilObj.i_booked_seat = 0
            assDeatilObj.i_cash = Cash
            assDeatilObj.t_remark = request.POST.get("Remark")
            assDeatilObj.i_status = CurTripStatus.Ing
            assDeatilObj.status = True
            assDeatilObj.save()
            data = {
                "Code": 100,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
                "Id": id,
            }
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "下单成功，去分享", data), content_type="application/json")
        except:
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "数据存储出错，请联系客服"), content_type="application/json")



def GetList(request):
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



        allMyAss = CarPoolingAssDetail.objects.filter(status=True).filter(c_userid=request.session["w_openid"]).order_by("-d_go_time")
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
                CardOwner=i.c_card_owner,
                UserId=i.c_userid,
                BusType=i.c_bus_type,
                Line=i.t_line,
                Seat=i.i_no_booked_seat,  # 余座
                BookedSeat=i.i_booked_seat, # 定座
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
        return HttpResponse(json.dumps(resultDict), content_type="application/json")

def Del(request):
    '''删除用户行程记录'''
    if request.method == "POST":
        id = request.POST.get("id")
        try:
            assObj = CarPoolingAssDetail.objects.get(c_id=id)
            if assObj.i_status == 1 or assObj.i_status == 2:
                return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "只有已完成的行程才可以删除"), content_type="application/json")
            assObj.status = False
            assObj.save()
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "删除成功"), content_type="application/json")
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "删除失败，联系管理员"), content_type="application/json")