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
    :return:{"Id":"4177159e-898c-4cc5-91ac-cc38c62e3c10","Phone":"186****5651","Name":"小杨","Sex":null,"IsEnabled":1,"OpenId":"oW0VHwSUAin2HoK0rtILIOEQr4iM","Dalance":"0.0","CreditValue":"1.7","Photo":"http://thirdwx.qlogo.cn/mmopen/7mqA5zvhhKa7mLMF5WEWeORyKG0GEfhq2hRrgib3aKGGn2GPAm2Xunial4rTLnTibEgmtvcudibC0T5dru92k8aBmBZSKwpp5LE9/132","BlackNote":null,"IsRealName":0,"IsRealDriver":0,"LastChangePhone":null,"UnedAssCount":0}
    '''
    if request.method == "POST":
        try:
            c_weixin_id = request.session["c_weixin_id"]
            userconfObj = CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
            dictItem = dict(
                Id = c_weixin_id,
                Phone = userconfObj.c_phone,
                Name = userconfObj.c_name,
                Sex = None,
                IsEnabled = userconfObj.status,
                OpenId = None,
                Dalance = userconfObj.i_cumulative_sum,
                CreditValue = userconfObj.i_cumulative_sum,
                Photo = "", # 图片地址
                BlackNote = "",
                IsRealName = "", #是否实名认证
                IsRealDriver = "",  #是否驾驶认证
                LastChangePhone = "", #上次修改电话的时间
                UnedAssCount = "",  # 车主未结束的账户数量
            )
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok",dictItem), content_type="application/json")
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "系统出错"), content_type="application/json")


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

def GetDalanceLogList(request):
    '''
    获取用户交易信息
    :param request:
    :return: {"DataSource":[{"User":null,"CreateTimeStr":"2018-05-01 18:10","Id":"00000000-0000-0000-0000-000000000000","UserId":"00000000-0000-0000-0000-000000000000","Code":null,"Action":0,"Money":10.00,"NowMoney":0.00,"CreateTime":"\/Date(1550820130579)\/","Note":"车主支付欠款","Remark":null}
    '''
    dictItem = [{"User":None,"CreateTimeStr":"2018-05-01 18:10","Id":"00000000-0000-0000-0000-000000000000","UserId":"00000000-0000-0000-0000-000000000000","Code":None,"Action":0,"Money":10.00,"NowMoney":0.00,"CreateTime":"\/Date(1550820130579)\/","Note":"车主支付欠款","Remark":None}]
    return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok",dictItem), content_type="application/json")
