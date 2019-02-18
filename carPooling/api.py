import json
import requests
import traceback
from django.shortcuts import render,HttpResponse
from common import client



# Create your views here.
def GetCityList(request):
    '''
    原文是post请求
    :param request:
    :return:  {Details:[{Name,"",Group:""}],Group:[FirstName,FullName]}
    '''
    if request.method == "POST":
        try:
            response = requests.post("http://lw.51bc.cc/WebApp/Home/GetCityList",timeout=5)
            cityList = response.content
            return HttpResponse(json.dumps(json.loads(cityList)), content_type="application/json")
        except:
            pass


        GroupList = [{"FirstName":"L","FullName":"L"},{"FirstName":"C","FullName":"C"}]
        DetailList = [{"Name":"泸定县","Group":"L"},{"Name":"成都","Group":"C"}]
        dictItem = dict(
            Details=DetailList,
            Group=GroupList
        )
        return HttpResponse(json.dumps(dictItem), content_type="application/json")



def GetHotLine(request):
    if request.method == "POST":
        try:
            response = requests.post("http://lw.51bc.cc/WebApp/Home/GetHotLine", timeout=5)
            hotlineList = response.content
            return HttpResponse(json.dumps(json.loads(hotlineList)),content_type="application/json")
        except:
            pass

        hotlineList = [{"StartCity": "成都", "EndCity": "泸定县", "Num": 0}]
        return HttpResponse(json.dumps(hotlineList), content_type="application/json")


def GetCurTripTip(request):
    return HttpResponse()

def GetAssList(request):
    if request.method == "POST":
        try:
            data = client.get_post_body(request)   #b'pageNum=1&numPerPage=20&startCity=%E6%88%90%E9%83%BD&endCity=%E5%B7%B4%E4%B8%AD&seatNum=1&goTime=null&lastId=null'
            response = requests.post("http://lw.51bc.cc/WebApp/Home/GetAssList",data=data, timeout=5,headers={"Content-Type":"application/x-www-form-urlencoded"})
            assList = response.content
            return HttpResponse(json.dumps(json.loads(assList)), content_type="application/json")
        except:
            # print(traceback.print_exc())
            pass

        assList = {"DataSource":[{"Id":"930302a5-565e-462b-84c4-abcd10922796","GoTime":"2019/2/20 9:00:00","CardOwner":"周正","UserId":"758038ca-84dc-4073-ace7-2616952db52b","BusType":"福特福睿斯。","Line":"温江出发，到达达州南外。","Cash":120.00,"Remark":"顺路上下，支持群价，预订后请电话确认一下。--点击“预订”即可，李。","Seat":2,"GoodNum":0,"BadNum":0,"IsRealName":0,"IsRealDriver":0}],
                "CurrentPageIndex":1,
                "PageSize":20,
                "RowCount":1,
                "PageCount":1,
                "IsFirstPage":"true",
                "IsLastPage":"true",
                "CurrentRowCount":1,
                "CurrentStartIndex":1,
                "CurrentEndIndex":1,
        }
        return HttpResponse(json.dumps(assList), content_type="application/json")