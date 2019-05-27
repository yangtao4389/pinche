from re import compile
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from common import client
from logging import getLogger
logger = getLogger("default")


extra_urls = ["/WebApp/Home/WeixinLogin","/WebApp/Home/WeiXinLoginCallBack"]
must_login_urls = [
    (r'/WebApp/*'),
]



must_login_urls_compile = [compile(expr) for expr in must_login_urls]

class MustCarpoolloginRequest(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info
        # 实现微信登录
        if any(m.match(path) for m in must_login_urls_compile) and path not in extra_urls:
            logger.info("MustCarpoolloginRequest:每一次进入的url记录：%s" % client.get_client_current_full_path(request))
            # request.session["w_openid"] = "oSczv05h7ZJ6KISCTfOeZ3SOel2M"  # 发布用户
            request.session["w_openid"] = "11111122222222"  # 预定用户
            w_openid = request.session.get('w_openid')
            logger.info("session中用户id：%s" % (w_openid))
            if not w_openid:
                request.session["tmp_current_full_url"] = client.get_client_current_full_path(request)
                return HttpResponseRedirect(extra_urls[0])


