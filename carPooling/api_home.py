import json
import requests
import traceback
import time
from enum import Enum
from datetime import datetime
from django.shortcuts import render,HttpResponse
from common import client,checkparam
from carPooling.models import CarPoolingCity,CarPoolingAssDetail,CarPoolingRecDetail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from common.json_result import RtnDefault,RtnCode
from carPooling.globalApi import commonGetCurTripTip
from logging import getLogger
logger = getLogger("default")

# Create your views here.
def GetCityList(request):
    '''
    原文是post请求
    :param request:
    :return:  {Details:[{Name,"",Group:""}],Group:[FirstName,FullName]}
    '''
    if request.method == "POST":
        # try:
        #     response = requests.post("http://lw.51bc.cc/WebApp/Home/GetCityList",timeout=5)
        #     cityList = response.content
        #     return HttpResponse(json.dumps(json.loads(cityList)), content_type="application/json")
        # except:
        #     pass
        # grouplist = CarPoolingCity.get_all_groups()
        # print(grouplist,"grouplist")
        # for i in grouplist:
        #     print(i.c_firstname)
        cityobjects = CarPoolingCity.get_all_city()
        GroupList = []
        DetailList = []
        templist = []
        for i in cityobjects:
            group = i.c_firstname
            if group not in templist:
                groupitem = dict(
                    FirstName = i.c_firstname,
                    FullName =  i.c_firstname,
                )
                GroupList.append(groupitem)
                templist.append(i.c_firstname)
            detailitem = dict(
                Name=i.c_fullname,
                Group=i.c_firstname,
            )
            DetailList.append(detailitem)
        # GroupList = [{"FirstName":"L","FullName":"L"},{"FirstName":"C","FullName":"C"}]
        # DetailList = [{"Name":"泸定县","Group":"L"},{"Name":"成都","Group":"C"}]
        dictItem = dict(
            Details=DetailList,
            Group=GroupList
        )
        return HttpResponse(json.dumps(dictItem), content_type="application/json")



def GetHotLine(request):
    if request.method == "POST":
        # try:
        #     response = requests.post("http://lw.51bc.cc/WebApp/Home/GetHotLine", timeout=5)
        #     hotlineList = response.content
        #     return HttpResponse(json.dumps(json.loads(hotlineList)),content_type="application/json")
        # except:
        #     pass

        hotlineList = [{"StartCity": "成都", "EndCity": "泸定县", "Num": 0},{"StartCity": "成都", "EndCity": "康定", "Num": 0}]
        return HttpResponse(json.dumps(hotlineList), content_type="application/json")






def GetCurTripTip(request):
    '''
     Type = 2 # 1,预约，2 当前行程（乘客） ，3 当前行程（车主）
    :param request:
    :return:
    '''
    userid = request.session["c_weixin_id"]
    dataresult = commonGetCurTripTip(userid)
    print(dataresult)
    if dataresult.get("result") == 0:
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok", dataresult), content_type="application/json")
    else:
        return HttpResponse()




def GetAssList(request):
    if request.method == "POST":
        # try:
        #     data = client.get_post_body(request)   #b'pageNum=1&numPerPage=20&startCity=%E6%88%90%E9%83%BD&endCity=%E5%B7%B4%E4%B8%AD&seatNum=1&goTime=null&lastId=null'
        #     response = requests.post("http://lw.51bc.cc/WebApp/Home/GetAssList",data=data, timeout=5,headers={"Content-Type":"application/x-www-form-urlencoded"})
        #     assList = response.content
        #     return HttpResponse(json.dumps(json.loads(assList)), content_type="application/json")
        # except:
        #     # print(traceback.print_exc())
        #     pass
        # 出发城市与到达城市
        startCity = request.POST.get("startCity")
        endCity = request.POST.get("endCity")
        # if not startCity or not endCity:
        #     return
        print(startCity,endCity)

        # 每页数据
        numPerPage = request.POST.get("numPerPage", 20)
        # if not checkparam.isVaildInt(numPerPage):
        #     return
        numPerPage = abs(int(numPerPage))

        # 当前查询页
        pageNum = request.POST.get("pageNum",1)
        # if not checkparam.isVaildInt(pageNum):
        #     return
        pageNum = int(pageNum)

        # seatNum 剩余座位数
        seatNum = request.POST.get("seatNum", 1)
        # if not checkparam.isVaildInt(seatNum):
        #     return
        seatNum = abs(int(seatNum))

        # goTime 出发时间 2019-02-18
        goTime = request.POST.get("goTime")
        if goTime == "null":
            goTime = datetime.now()
        else:
            if not checkparam.isVaildDate(goTime):
                return
        # if not checkparam.isVaildDate(goTime):
        #     return
        print(goTime)
        # 备用字段
        lastId = request.POST.get("lastId","null")

        allAss = CarPoolingAssDetail.objects.filter(status=True).filter(c_start_city=startCity, c_end_city=endCity).filter(d_go_time__gte=goTime).filter(i_no_booked_seat__gte=seatNum)
        paginator = Paginator(allAss, numPerPage)
        page = paginator.page(pageNum)

        # "CurrentPageIndex": 1, "PageSize": 20, "RowCount": 66, "PageCount": 4, "IsFirstPage": true, "IsLastPage": false, "CurrentRowCount": 20, "CurrentStartIndex": 1, "CurrentEndIndex": 20
        resultDict = dict(
            CurrentPageIndex = pageNum,
            PageSize = numPerPage,
            RowCount = paginator.count,
            PageCount = paginator.num_pages,
            IsFirstPage = not page.has_previous(),
            IsLastPage = not page.has_next(),
            CurrentRowCount = page.__len__(),
            CurrentStartIndex = 1 if page.__len__() >= 1 else 0,
            CurrentEndIndex = page.__len__(),

        )
        DataSource = []
        for i in page.object_list:
            dictItem = dict(
                Id = i.c_id,
                GoTime = i.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                # GoTime = str(i.d_go_time),
                CardOwner = i.c_card_owner,
                UserId = i.c_userid,
                BusType = i.c_bus_type,
                Line = i.t_line,
                Seat = i.i_no_booked_seat,
                Cash = i.i_cash,
                GoodNum = 0,  # 点赞
                BadNum = 0,  # 差评
                IsRealName = 0, # 姓名是否有效
                IsRealDriver = 0,  # 身份是否验证
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
        logger.info(resultDict)
        return HttpResponse(json.dumps(resultDict), content_type="application/json")


def GetWenxinJsapiConfig():
    '''
    :return: {"debug":false,"appId":"wx56b24a9f02010e10","timestamp":"1550636346","nonceStr":"A7A1ECABE61CFF230F11EC241A825AD6","signature":"1b07f146fc7e34132db3fa0658c1f9ecb33f53fe","jsApiList":null}
    '''
    return HttpResponse()

def CheckWeiXinSubscribe():
    return HttpResponse()