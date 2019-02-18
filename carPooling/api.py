import json
import requests
from django.shortcuts import render,HttpResponse



'''



'''



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