import json
import requests
import traceback
from django.shortcuts import render,HttpResponse
from common import client
from common.json_result import RtnDefault,RtnCode



# Create your views here.
def GetDetailData(request):
    '''
    原文是post请求
    :param request:
    :return:  {Details:[{Name,"",Group:""}],Group:[FirstName,FullName]}
    '''



    if request.method == "POST":
        Id = request.POST.get("Id")
        print(Id)
        # if not Id:
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM,"没有id"), content_type="application/json")
        # data = '''
        #  {"statusCode":200,"message":"操作成功!","data":{"Id":"b8cf77a3-c671-4560-9bed-a746b8a52276","StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","GoTime":"2019/2/20 0:00:00","BusType":"丰田致炫","VehicleNumber":null,"Seat":3,"BookedSeat":0,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","Status":1,"UserId":"4177159e-898c-4cc5-91ac-cc38c62e3c10"}}
        # '''
        # 如果有记录，返回最后一条。如果没有，data直接返回
        data = {
            "Status": 1,  # 0代表提交成功，但未正常实现。1代表可以编辑，2代表行程结束
        }
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK,"新用户",data), content_type="application/json")


def GetLastAss(request):
    if request.method == "POST":
        StartCity = request.POST.get("StartCity")
        EndCity = request.POST.get("EndCity")
        # {"StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","Seat":3,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","BusType":"丰田致炫","VehicleNumber":null}
        # {"StartCity":"广元","EndCity":"成都","Line":"XX 出发，XX 站上高速，XX 站下高速，途径X 号线XX 地铁站（推荐下车点），最终目的地：XX","Seat":3,"Cash":100,"Remark":"顺路上下，支持群价，预订后请电话确认一下。","Phone":"18649715651","CardOwner":"小杨","BusType":null,"VehicleNumber":null}
        data = {"StartCity":"成都","EndCity":"巴中","Line":"武侯大道 出发，途径武侯大道地铁站（推荐上车点），巴中西 站下高速，目的地：巴中，仅限巴中市区可送。","Seat":3,"Cash":100.00,"Remark":"来呀，一起回家呀","Phone":"18649715651","CardOwner":"小杨","BusType":"丰田致炫","VehicleNumber":None}
        return HttpResponse(json.dumps(data),content_type="application/json")

def Cancel(request):
    if request.method == "POST":
        Id = request.POST.get("Id")
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "取消成功"), content_type="application/json")

def SaveEdit(request):
    if request.method == "POST":
        data = {
            "Code": 200,  # 100代表 分享，200代表去用户中心，300代表再次编辑？？
        }
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "新用户", data), content_type="application/json")
