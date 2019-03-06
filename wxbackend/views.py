from django.shortcuts import render, HttpResponse

from wxbackend import v_token_related, v_xml_related, v_midia, v_menu
from logging import getLogger

logger = getLogger("default")


# Create your views here.
def HandleExample(request):
    if request.method == "GET":
        # 验证token
        result = v_token_related.verifyToken(request)
    elif request.method == "POST":
        result = v_xml_related.xml_text(request)
    else:
        result = "非法请求"

    logger.info("所有回复的result：%s" % result)
    return HttpResponse(result)


def mediaHandle(request):
    myMedia = v_midia.Media()
    itemA = v_token_related.real_get_access_token()
    if not itemA:
        return HttpResponse("获取token失败")
    accessToken, exTime = itemA
    filePath = "media/images/2fab5afa6d.png"  # 请安实际填写
    mediaType = "image"
    result = myMedia.uplaodForever(accessToken, filePath, mediaType)
    return HttpResponse(result)


def menuHandle(request):
    myMenu = v_menu.Menu()
    postJson = """
       {
           "button":
           [
               {
                   "type": "click",
                   "name": "开发指引",
                   "key":  "mpGuide"
               },
               {
                   "name": "公众平台",
                   "sub_button":
                   [
                       {
                           "type": "view",
                           "name": "更新公告",
                           "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                       },
                       {
                           "type": "view",
                           "name": "接口权限说明",
                           "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
                       },
                       {
                           "type": "view",
                           "name": "返回码说明",
                           "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
                       }
                   ]
               },
               {
                   "type": "media_id",
                   "name": "旅行",
                   "media_id": "z2zOokJvlzCXXNhSjF46gdx6rSghwX2xOD5GUV9nbX4"
               }
             ]
       }
        """
    itemA = v_token_related.real_get_access_token()
    if not itemA:
        return HttpResponse("获取token失败")
    accessToken, exTime = itemA
    # myMenu.delete(accessToken)
    result = myMenu.create(postJson, accessToken)
    return HttpResponse(result)