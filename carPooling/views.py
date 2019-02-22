from datetime import datetime, timedelta
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from common import uuid_maker, client
from carPooling.models import CarPoolingUserConf, CarPoolingAssDetail
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
    try:
        c_weixin_id = "xxxxx"
        CarPoolingUserConf.objects.get_or_create(c_weixin_id=c_weixin_id)
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
        currentAss = CarPoolingAssDetail.objects.filter(c_userid=userid).filter(status=True).filter(
            d_go_time__gte=datetime.now() - timedelta(hours=2))
        if len(currentAss) > 0:
            if len(currentAss) > 1:
                logger.exception("当前用户：%s当前时间段:%s存在多个行程" % (userid, datetime.now()))
                return HttpResponse("请联系管理员")
            return HttpResponseRedirect("/WebApp/UserAss/Detail?id=%s" % currentAss[0].c_id)

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


def About(request):
    with open("static/carPooling/src/UserCenter.html", 'rb') as f:
        html = f.read()
    return HttpResponse(html)
