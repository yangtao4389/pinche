from django.shortcuts import HttpResponse
from logging import getLogger
logger = getLogger("default")

def JsError(request):
    if request.method == "POST":
        msg = request.POST.get('msg')
        logger.error("jsError:%s"%msg)
        print(msg)
        return HttpResponse()
