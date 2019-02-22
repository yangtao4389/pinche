from carPooling.models import CarPoolingUserConf
from common.json_result import RtnDefault,RtnCode
from django.shortcuts import render,HttpResponse,HttpResponseRedirect


def PhoneStatus(request):
    '''
    查看当前用户是否绑定电话
    :return:
    '''
    c_weixin_id = request.session["c_weixin_id"]
    try:
        userObj = CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
        if not userObj.b_phone_status:
            dataDict = dict(
                PhoneStatus=False,
            )
        else:
            dataDict = dict(
                PhoneStatus=True,
                Phone = userObj.c_phone
            )
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok",dataDict), content_type="application/json")
    except:
        return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "系统出错"), content_type="application/json")


def GetUserInfo(request):
    '''
    获取用户信息，全局用
    :param request:
    :return:
    '''
    if request.method == "POST":
        pass

def GetCodeLogin(request):
    '''
    获取短信验证码
    :param request:
    :return:
    '''
    pass

def SavePhone(request):
    '''
    保存电话号码
    :param request:
    :return:
    '''
    pass

