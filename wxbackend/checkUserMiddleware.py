from tools.common import client
from datetime import datetime
from re import compile
from django.http import HttpResponseRedirect, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from django.core.cache import cache
import os
from logging import getLogger
from wxbackend import v_token_related
import datetime

logger = getLogger("default")


def refreshToken(request):
    ret = v_token_related.getToken()
    if ret:
        access_token, expires_in = ret
        nowDatetime = datetime.datetime.now()
        request.session['access_token'] = access_token
        request.session['expires_time'] = nowDatetime + datetime.timedelta(seconds=expires_in)
    else:
        raise Exception("更新token错误，检查服务器")

class CheckUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        logger.info("每一次进入的url记录：%s" % client.get_client_current_full_path(request))
        access_token = request.session.get('access_token')
        if not access_token:
            refreshToken(request)
        if access_token:
            expires_time = request.session['expires_time']
            if datetime.datetime.now() > expires_time:
                refreshToken(request)

