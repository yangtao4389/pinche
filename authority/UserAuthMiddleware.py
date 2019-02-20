# -*- coding: utf-8 -*-
from re import compile
from django.http import HttpResponseRedirect
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

EXEMPT_URLS = [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]
# if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
#     EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class UserAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if 'c_weixin_id' not in request.session or not request.session['c_weixin_id']:
            path = request.path_info
            if not any(m.match(path) for m in EXEMPT_URLS):
                # print path
                return HttpResponseRedirect(settings.LOGIN_URL)
