import json
import requests
import traceback
from datetime import datetime,timedelta
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.conf import settings
from common import client,uuid_maker,checkparam
from common.json_result import RtnDefault,RtnCode
from carPooling.models import CarPoolingAssDetail,CarPoolingUserConf,CarPoolingCity
from logging import getLogger
logger = getLogger("default")


# Create your views here.
def GetDetailData(request):
    '''
    原文是post请求
    :param request:
    :return:  {Details:[{Name,"",Group:""}],Group:[FirstName,FullName]}
    '''
    if request.method == "POST":
        Id = request.POST.get("Id")
        if not Id:
            Id = uuid_maker.get_uuid_random()

        try:
            # 去数据库查看当前Id是否存在
            CarPoolingAssDetail.objects.get(c_id=Id)
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "已下过单用户"), content_type="application/json")
        except:
            # 没有数据
            dataDict = dict(
                Id = Id,
                UserId = request.session["c_weixin_id"],
                Status= 1,
                # GoTime = datetime.strftime(datetime.now() + timedelta(minutes=10),"%Y-%m-%d %H:%M:%S")
            )
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK,"未下过单用户",dataDict), content_type="application/json")
        # # print(Id)
        # if not Id:
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM,"没有id"), content_type="application/json")
        # data = '''
        #  {"statusCode":200,"message":"操作成功!","data":{"Id":"b8cf77a3-c671-4560-9bed-a746b8a52276","StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","GoTime":"2019/2/20 0:00:00","BusType":"丰田致炫","VehicleNumber":null,"Seat":3,"BookedSeat":0,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","Status":1,"UserId":"4177159e-898c-4cc5-91ac-cc38c62e3c10"}}
        # '''
        # 如果有记录，返回最后一条。如果没有，data直接返回
        # data = {
        #     "Status": 1,  # 0代表提交成功，但未正常实现。1代表可以编辑，2代表行程结束
        # }
        # return HttpResponse(RtnDefault(RtnCode.STATUS_OK,"新用户",data), content_type="application/json")


def GetLastAss(request):
    '''
    时刻去请求，可能是保存页面其它内容用
    :param request:
    :return:
    '''
    if request.method == "POST":
        StartCity = request.POST.get("StartCity")
        EndCity = request.POST.get("EndCity")
        # print(StartCity,EndCity)
        if StartCity != "undefined" and EndCity != "undefined":
            data = {"StartCity": StartCity, "EndCity": EndCity}
        elif StartCity != "undefined" and EndCity == "undefined":
            data = {"StartCity": StartCity, "EndCity": "成都"}
        elif  StartCity == "undefined" and EndCity != "undefined" :
            data = {"StartCity": "成都", "EndCity": EndCity}
        else:
            data = {"StartCity": "成都", "EndCity": "成都"}

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
        # data = {"StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","Seat":3,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","BusType":"丰田致炫","VehicleNumber":None}

        return HttpResponse(json.dumps(data),content_type="application/json")

def Cancel(request):
    if request.method == "POST":
        Id = request.POST.get("Id")
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "取消成功"), content_type="application/json")

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
        try:
            assDeatilObj,created = CarPoolingAssDetail.objects.get_or_create(c_id=Id)
            userObj = CarPoolingUserConf.objects.get(c_weixin_id=request.session["c_weixin_id"])
        except:
            # 用户id不存在，直接去login页面
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            return HttpResponseRedirect(settings.LOGIN_URL)



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

        # VehicleNumber = request.POST.get("VehicleNumber")
        # if VehicleNumber and not checkparam.isVaildInt(VehicleNumber):

        Seat=request.POST.get("Seat")
        if not checkparam.isVaildInt(Seat):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座出错"), content_type="application/json")
        Seat = int(Seat)
        if Seat>6:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "余座不应该大于6位"), content_type="application/json")

        Cash = request.POST.get("Cash")
        if not checkparam.isVaildInt(Cash):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "费用出错"), content_type="application/json")
        Cash = int(Cash)
        if Cash>200:
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "设置费用过高"), content_type="application/json")

        try:
            assDeatilObj.c_userid = userObj.c_weixin_id
            assDeatilObj.c_card_owner = userObj.c_name
            assDeatilObj.c_user_phone = userObj.c_phone
            assDeatilObj.c_start_city =StartCity
            assDeatilObj.c_end_city =EndCity
            assDeatilObj.t_line = request.POST.get("Line")
            assDeatilObj.d_go_time = GoTime
            assDeatilObj.c_bus_type = request.POST.get("BusType")
            # assDeatilObj.i_vehicle_number = None
            assDeatilObj.i_seat = Seat
            assDeatilObj.i_booked_seat = 0
            assDeatilObj.i_cash = Cash
            assDeatilObj.t_remark = request.POST.get("t_remark")
            assDeatilObj.status = True
            assDeatilObj.save()
        except:
            print(traceback.print_exc())
            logger.exception("save ass detail error")
            data = {
                "Code": 300,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
            }
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "数据存储出错，请联系客服"), content_type="application/json")
        # StartCity = request.POST.get("StartCity")
        # EndCity = request.POST.get("EndCity")
        # GoTime = request.POST.get("GoTime")
        # GoTimeShow = request.POST.get("GoTimeShow")
        # Cash = request.POST.get("Cash")
        # BusType = request.POST.get("BusType")
        # VehicleNumber = request.POST.get("VehicleNumber")
        # Seat = request.POST.get("Seat")
        # Remark = request.POST.get("Remark")
        # Line = request.POST.get("Line")
        # # c_id = "%s%s" % (uuid_maker.UIDMaker_DateTime_obj(),Id)
        # # 订单号生成规则：日期：时间戳10位 + 用户4位最后id
        # CarPoolingAssDetail.objects.create(
        #     c_id = uuid_maker.get_uuid_random(),
        #     c_userid = uuid,
        #     StartCity = StartCity,
        #     EndCity = EndCity,
        #     GoTime = GoTime,
        #     GoTimeShow = GoTimeShow,
        #
        # )


        data = {
            "Code": 200,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
        }
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "下单成功，去分享", data), content_type="application/json")
