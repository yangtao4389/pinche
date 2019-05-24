import re
import random
from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from common import uuid_maker, client,checkparam
from carPooling.models import CarPoolingUserConf, CarPoolingAssDetail
from carPooling.globalApi import commonGetCurTripTip
from common.json_result import RtnDefault,RtnCode
from app_weixin.settings import wx_login
from . import settings
from logging import getLogger
logger = getLogger("default")


# Create your views here.
def Home(request):
    # return HttpResponseRedirect("/static/carPooling/src/Home.html")
    with open("static/carPooling/src/Home.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def WeixinLogin(request):
    '''
    微信登录，获取用户的昵称，可能过后需要获取用户的定位等。获取用户的全部信息，拿到昵称，头像，城市，
    :param request:
    :return:
    '''
    # 获取参数：
    snsapi_userinfo = request.GET.get("snsapi_userinfo") # true,false


    LIST = ["a","b","c","d","e","f",'g','h','i',"1","2","H","K"]
    w_tmp_state =  "".join(random.sample(LIST, 5))
    request.session["w_tmp_state"] = w_tmp_state

    redirect_uri = settings.WX_DOMAIN + reverse("WeiXinLoginCallBack")  #/WebApp/Home/WeiXinLoginCallBack
    url = wx_login.authorize(client.decode_url(redirect_uri), "snsapi_base",state=w_tmp_state)      # 实现数据库用的用户直接登录，不用再次授权

    if snsapi_userinfo == "true":
        redirect_uri += "?&snsapi_userinfo=true"
        url = wx_login.authorize(client.decode_url(redirect_uri), "snsapi_userinfo",state=w_tmp_state)  # 获取用户信息是在发现数据库没有该用户的时候决定
    logger.info("获取code的url：%s"%url)
    return HttpResponseRedirect(url)

def WeiXinLoginCallBack(request):
    '''
    正常情况应该获取到用户的code跟state
    :param request:
    :return:
    '''
    w_code = request.GET.get("code")
    w_state = request.GET.get("state")
    snsapi_userinfo = request.GET.get("snsapi_userinfo")

    if not w_code or w_state!=request.session.get("w_tmp_state"):
        return HttpResponse("验证失败，尴尬")
    data = wx_login.access_token(w_code)
    logger.info("微信验证用户数据获取的data:%s"%data)
    logger.info("微信验证用户数据获取的refresh_token:%s"%data.refresh_token)

    userconf,created = CarPoolingUserConf.objects.get_or_create(w_openid = data.openid)
    if created:
        return HttpResponseRedirect(reverse("WeixinLogin")+"?&snsapi_userinfo=true" )
    # 非创建，如果来自snsapi_userinfo 则更新数据
    if snsapi_userinfo == "true":
        # 该refresh_token 的有效期为30天。也就是当access_token 2分钟后失效时可以用refresh_token刷新来重新获取
        #{'openid': 'oSczv05h7ZJ6KISCTfOeZ3SOel2M', 'scope': 'snsapi_userinfo', 'access_token': '21_wPXARwQVWCsdmpfHsIpnn0RRufKCTMfhMvSMQcUEA1ZqP2hkm-7K_rUBZZjUZbH2X32pQiZv2HfloiulsWJ2Fw', 'errcode': {}, 'refresh_token': '21_b2-zR21o0Qc_K_xeNBkBSHPnzvpWgM2o2gnnOSiUb416kb7Z-FLP-rA5pQmiRnD2BwQQh0eKYJcUWIffjUg0GA', 'expires_in': 7200}

        # 刷新令牌 获取用户信息
        # r_data = wx_login.refresh_token(data.refresh_token)
        # logger.info("刷新令牌后数据获取的data:%s" % r_data)

        # 如果创建，再去请求获取用户信息，这里携带具体的参数回调
        u_data = wx_login.userinfo(data.access_token,data.openid)

        # if (datetime.now() - userconf.update_time).total_seconds() > 60*60*72: # datetime.now() - userconf.update_time得到datetime.timedelta(0, 68, 269473)  三天没更新过才去更新
        userconf.w_nickname = u_data.nickname
        userconf.w_sex = u_data.sex
        userconf.w_country = u_data.country
        userconf.w_province = u_data.province
        userconf.w_city = u_data.city
        userconf.w_headimgurl = u_data.headimgurl
        userconf.save()


    request.session["w_openid"] = data.openid
    # openid = data.openid
    next_url = request.session.get("tmp_current_full_url","/WebApp/Home")
    return HttpResponseRedirect(next_url)
    # return HttpResponse("ok")


def Login(request):
    '''
    登录创建数据表
    :param request:
    :return:
    '''
    # 微信端会传送过来微信id
    # 如果微信id存在，则去数据库查询。如果没有电话信息，则弹绑定手机，如果有，则存session
    # 不存在，则非法访问（提示需要在微信客户端打开）
    if request.method == 'GET':
        # c_weixin_id = uuid_maker.get_uuid_random()
        # c_weixin_id = client.get_client_ip(request)
        # # c_weixin_id = "f71f615f-2fb1-49a1-adfa-6978ac2decf7"
        # entry_url = client.get_client_previous_url(request)
        # request.session['entry_url'] = entry_url
        # try:
        #     userObj = CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
        #     if userObj.c_phone and userObj.b_phone_status == True:
        #         request.session['c_weixin_id'] = c_weixin_id
        #         return HttpResponseRedirect(entry_url)
        # except:
        #     logger.info("该用户不存在")
        # request.session['tmp_weixin_id'] = c_weixin_id
        # 数据库不存在，则表示未创建，需要直接去登录页。
        with open("static/carPooling/src/Login.html", 'rb') as f:
            html = f.read()
        return HttpResponse(html)

    elif request.method == 'POST':
        # 这一步是微信登录，暂且取消
        # tmp_weixin_id = request.session.get("tmp_weixin_id")
        # if not tmp_weixin_id:
        #     return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "请刷新页面重试"), content_type="application/json")
        realName = request.POST.get("realName")
        PhoneNum = request.POST.get("PhoneNum")
        smsCode = request.POST.get("smsCode")
        if not checkparam.checkTelPhone(PhoneNum):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "电话号码出错"), content_type="application/json")
        if smsCode != request.session.get("smsCode"):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "电话验证码出错"), content_type="application/json")

        try:
            tmp_weixin_id = uuid_maker.get_uuid_random()
            carobj,created = CarPoolingUserConf.objects.get_or_create(c_phone=PhoneNum)
            if created:
                carobj.c_weixin_id = tmp_weixin_id
                carobj.c_name = realName
                carobj.b_phone_status = True
                carobj.i_cumulative_sum = 10
                carobj.status = True
                carobj.save()

            #
            # CarPoolingUserConf(
            #     c_weixin_id = tmp_weixin_ip,  # 暂时存ip
            #     c_name = realName,
            #     c_phone = PhoneNum,
            #     b_phone_status = True,
            #     i_cumulative_sum = 10,
            #     status = True,
            # ).save()
            goUrl = request.session.get('entry_url') if request.session.get('entry_url') else "/WebApp/Home"
            request.session['c_weixin_id'] = tmp_weixin_id
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "登录成功",dict(goUrl=goUrl)), content_type="application/json")
        except:
            logger.exception("创建用户数据出错")
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "系统出错"), content_type="application/json")

    #
    # try:
    #     # c_weixin_id = "xxxxx"
    #     c_weixin_id = uuid_maker.get_uuid_random()
    #     CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
    #     request.session["c_weixin_id"] = c_weixin_id
    #     # print(client.get_client_previous_url(request))
    #     # return HttpResponseRedirect(client.get_client_previous_url(request))
    #     return HttpResponseRedirect("/WebApp/Home")
    # except:
    #     logger.exception("login error")
    #     with open("static/carPooling/src/Error.html", 'rb') as f:
    #         html = f.read()
    #     return HttpResponse(html)


def AssList(request):
    with open("static/carPooling/src/Asslist.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def AssShareTip(request):
    with open("static/carPooling/src/AssShareTip.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserAssPublish(request):
    id = request.GET.get("id")
    if not id:
        # todo 去数据库查询当前的状态，如果有发布信息，则返回当前车程状态，未发布，则创建新的id.
        w_openid = request.session["w_openid"]
        dataresult = commonGetCurTripTip(w_openid)
        if dataresult.get("result") == 0:
            return HttpResponseRedirect(dataresult.get("redirectUrl"))

        id = uuid_maker.get_uuid_random()
        return HttpResponseRedirect(
            client.get_client_current_path(request) + "?" + client.get_client_query_str(request) + "id=" + id)
    else:
        # 有id，验证来源,如果是存在的，那么就代表是分享过后的返回
        try:
            CarPoolingAssDetail.objects.get(c_id=id)
            return HttpResponseRedirect("/WebApp/UserAss/Detail?id=%s" % id)
        except:
            with open("static/carPooling/src/UserAssPublish.html", 'rb') as f:
                html = f.read()
            return HttpResponse(html)


def UserAssDetail(request):
    id = request.GET.get("id")
    if not id:
        return HttpResponse("无id")
    with open("static/carPooling/src/UserAssDetail.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserAssList(request):
    with open("static/carPooling/src/UserAssList.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserAssEdit(request):
    with open("static/carPooling/src/UserAssEdit.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserRecList(request):
    with open("static/carPooling/src/UserRecList.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserRecDetail(request):
    with open("static/carPooling/src/UserRecDetail.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserCenter(request):
    with open("static/carPooling/src/UserCenter.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def UserCenterChangePhone(request):
    if request.method == 'GET':
        with open("static/carPooling/src/ChangePhone.html", 'rb') as f:
            html = f.read()
        return HttpResponse(html)
    elif request.method == 'POST':
        newPhoneNum = request.POST.get("newPhoneNum")
        smsCode = request.POST.get("smsCode")
        if not checkparam.checkTelPhone(newPhoneNum):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "电话号码出错"), content_type="application/json")
        if smsCode != request.session.get("smsCode"):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "验证码出错"), content_type="application/json")
        try:
            userObj = CarPoolingUserConf.objects.get(w_openid=request.session["w_openid"])
            userObj.c_phone = newPhoneNum
            userObj.save()
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "修改成功"), content_type="application/json")
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "保存失败"), content_type="application/json")




def UserCenterDalanceLogList(request):
    with open("static/carPooling/src/DalanceLogList.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def About(request):
    with open("static/carPooling/src/UserCenter.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


def AboutCreditValueNote(request):
    with open("static/carPooling/src/CreditValueNote.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)
