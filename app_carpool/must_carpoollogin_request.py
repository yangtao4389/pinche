from re import compile
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from logging import getLogger
logger = getLogger("default")


extra_urls = ["/WebApp/Home/Login","/WebApp/Home/Register"]
must_login_urls = [
    (r'/WebApp/Home/*'),
]
must_login_urls_compile = [compile(expr) for expr in must_login_urls]

class MustCarpoolloginRequest(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        if any(m.match(path) for m in must_login_urls_compile) and path not in extra_urls:
            print(path)
            sessionUserId = request.session.get('c_weixin_id')
            logger.info("session中用户id：%s" % (sessionUserId))
            if not sessionUserId:
                return HttpResponseRedirect(extra_urls[0])
