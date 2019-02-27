import os
from common import client
from re import compile
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
# from carPooling.models import ServiceUserConf, ServiceCityCdn
# from statistic.tasks import statistic_pv
from logging import getLogger
logger = getLogger("default")


def get_key_from_value(dict_item, value):
    return list(dict_item.keys())[list(dict_item.values()).index(value)]


EXEMPT_URLS = [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class CheckUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        logger.info("每一次进入的url记录：%s" % client.get_client_current_full_path(request))
        useragent = client.get_client_HTTP_USER_AGENT(request)
        logger.info("每一次进入的useragent记录：%s" % useragent)
        logger.info("每一次进入用户ip：%s" % client.get_client_ip(request))
        # return HttpResponseRedirect("http://112.18.251.47:8801/hall/index.do")
        # request.session['userid'] = "checkuser"
        if not any(m.match(path) for m in EXEMPT_URLS):
            # if useragent.find("Mozilla/5.0") != -1:
            #     return HttpResponse("error")

            # 验证用户id
            sessionUserId = request.session.get('c_weixin_id')
            logger.info("session中用户id：%s" % (sessionUserId))
            if not sessionUserId :
                # 初始化
                return HttpResponseRedirect(settings.LOGIN_URL)


            # # 统计pv
            # userid = request.session['userid']
            # # carrierId = request.session['cityCode']
            # carrierId = ""
            # c_product = settings.PRODUCT_KEY
            # path_list = path.split("/")[1:]  # 去掉第一个['', 'hall', 'index.do', '']
            # if os.name != "posix":
            #     statistic_pv(userid, carrierId, c_product, *path_list)
            # else:
            #     statistic_pv.delay(userid, carrierId, c_product, *path_list)  # 开启celery去执行
            # logger.info("用户初始化完成")
