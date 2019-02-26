from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from common import uuid_maker, client,checkparam
from carPooling.models import CarPoolingUserConf, CarPoolingAssDetail
from carPooling.globalApi import commonGetCurTripTip
from common.json_result import RtnDefault,RtnCode
from logging import getLogger
logger = getLogger("default")


# Create your views here.
def Home(request):
    # return HttpResponseRedirect("/static/carPooling/src/Home.html")
    with open("static/carPooling/src/Home.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


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
        c_weixin_id = uuid_maker.get_uuid_random()
        entry_url = client.get_client_previous_url(request)
        request.session['entry_url'] = entry_url
        try:
            userObj = CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
            if userObj.c_phone and userObj.b_phone_status == True:
                request.session['c_weixin_id'] = c_weixin_id
                return HttpResponseRedirect(entry_url)
        except:
            logger.info("该用户不存在")
        request.session['tmp_weixin_id'] = c_weixin_id
        # 数据库不存在，则表示未创建，需要直接去登录页。
        with open("static/carPooling/src/Login.html", 'rb') as f:
            html = f.read()
        return HttpResponse(html)

    elif request.method == 'POST':
        tmp_weixin_id = request.session.get("tmp_weixin_id")
        if not tmp_weixin_id:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "请刷新页面重试"), content_type="application/json")
        realName = request.POST.get("realName")
        PhoneNum = request.POST.get("PhoneNum")
        smsCode = request.POST.get("smsCode")
        if not checkparam.checkTelPhone(PhoneNum):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "电话号码出错"), content_type="application/json")
        if smsCode != request.session.get("smsCode"):
            return HttpResponse(RtnDefault(RtnCode.STATUS_PARAM, "电话验证码出错"), content_type="application/json")

        try:
            CarPoolingUserConf(
                c_weixin_id = tmp_weixin_id,
                c_name = realName,
                c_phone = PhoneNum,
                b_phone_status = True,
                i_cumulative_sum = 10,
                status = True,
            ).save()
            goUrl = request.session.get('entry_url') if request.session.get('entry_url') else "/WebApp/Home"
            request.session['c_weixin_id'] = tmp_weixin_id
            return HttpResponse(RtnDefault(RtnCode.STATUS_OK, "登录成功",dict(goUrl=goUrl)), content_type="application/json")
        except:
            return HttpResponse(RtnDefault(RtnCode.STATUS_SYSERROR, "系统出错"), content_type="application/json")





    try:
        # c_weixin_id = "xxxxx"
        c_weixin_id = uuid_maker.get_uuid_random()
        CarPoolingUserConf.objects.get(c_weixin_id=c_weixin_id)
        request.session["c_weixin_id"] = c_weixin_id
        # print(client.get_client_previous_url(request))
        # return HttpResponseRedirect(client.get_client_previous_url(request))
        return HttpResponseRedirect("/WebApp/Home")
    except:
        logger.exception("login error")
        with open("static/carPooling/src/Error.html", 'rb') as f:
            html = f.read()
        return HttpResponse(html)


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
        userid = request.session["c_weixin_id"]
        dataresult = commonGetCurTripTip(userid)
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


def UserCenterPhone(request):
    with open("static/carPooling/src/Phone.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)


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
