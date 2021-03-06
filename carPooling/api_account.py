import time
from datetime import datetime,timedelta
from carPooling.models import CarPoolingUserConf
from common.json_result import RtnDefault,RtnCode
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from common import checkparam
from eventNotice import smsSend
from app_weixin.settings import logger


def PhoneStatus(request):
    '''
    查看当前用户是否绑定电话
    :return:
    '''
    w_openid = request.session["w_openid"]
    try:
        userObj = CarPoolingUserConf.objects.get(w_openid=w_openid)
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
        logger.exception("电话号码状态验证失败")
        return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "系统出错"), content_type="application/json")


def GetUserInfo(request):
    '''
    获取用户信息，全局用
    :param request:
    :return:{"Id":"4177159e-898c-4cc5-91ac-cc38c62e3c10","Phone":"186****5651","Name":"小杨","Sex":null,"IsEnabled":1,"OpenId":"oW0VHwSUAin2HoK0rtILIOEQr4iM","Dalance":"0.0","CreditValue":"1.7","Photo":"http://thirdwx.qlogo.cn/mmopen/7mqA5zvhhKa7mLMF5WEWeORyKG0GEfhq2hRrgib3aKGGn2GPAm2Xunial4rTLnTibEgmtvcudibC0T5dru92k8aBmBZSKwpp5LE9/132","BlackNote":null,"IsRealName":0,"IsRealDriver":0,"LastChangePhone":null,"UnedAssCount":0}
    '''
    if request.method == "POST":
        try:
            w_openid = request.session["w_openid"]
            userconfObj = CarPoolingUserConf.objects.get(w_openid=w_openid)
            dictItem = dict(
                Id = w_openid,
                Phone = userconfObj.c_phone,
                Name = userconfObj.c_name,
                Sex = None,
                IsEnabled = userconfObj.status,
                OpenId = w_openid,
                Dalance = userconfObj.i_cumulative_sum,
                CreditValue = userconfObj.i_cumulative_sum,
                Photo = userconfObj.w_headimgurl, # 图片地址
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
    if request.method == "POST":
        phone = request.POST.get("phone")
        imgCode = request.POST.get("code")
        if not checkparam.checkTelPhone(phone):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "参数出错"), content_type="application/json")
        # 全局短信验证码：
        smsCode =checkparam.generate_code(4)
        request.session["smsCode"] = smsCode
        last_sms_send_time = request.session.get("last_sms_send_time")
        now = time.time()
        request.session["last_sms_send_time"] = now
        if last_sms_send_time:
            if now-60 < last_sms_send_time:
                logger.info("发送频率过快")
                return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "发送频率过快"), content_type="application/json")

        smsSend.smsSend(phone, smsCode)
        return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "发送成功"), content_type="application/json")







def GetDalanceLogList(request):
    '''
    获取用户交易信息
    :param request:
    :return: {"DataSource":[{"User":null,"CreateTimeStr":"2018-05-01 18:10","Id":"00000000-0000-0000-0000-000000000000","UserId":"00000000-0000-0000-0000-000000000000","Code":null,"Action":0,"Money":10.00,"NowMoney":0.00,"CreateTime":"\/Date(1550820130579)\/","Note":"车主支付欠款","Remark":null}
    '''
    dictItem = [{"User":None,"CreateTimeStr":"2018-05-01 18:10","Id":"00000000-0000-0000-0000-000000000000","UserId":"00000000-0000-0000-0000-000000000000","Code":None,"Action":0,"Money":10.00,"NowMoney":0.00,"CreateTime":"\/Date(1550820130579)\/","Note":"车主支付欠款","Remark":None}]
    return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "ok",dictItem), content_type="application/json")
