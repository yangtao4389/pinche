from django.shortcuts import HttpResponse

from .settings import myrobotclient, myrobot


def createMenu(request):
    myrobotclient.create_menu({
        "button": [
            {
                "type": "click",
                "name": "我要拼车",
                "key": "key1"
            },
            {
                "type": "view",
                "name": "拼车首页",
                "url": "http://211.149.180.119/WebApp/Home"
            },
            {
                "name": "我的",
                "sub_button": [
                    {
                        "type": "view",  # web页面
                        "name": "搜索",
                        "url": "http://www.soso.com/"
                    },
                    {
                        "type": "miniprogram",  # 小程序
                        "name": "万年历",
                        "url": "http://mp.weixin.qq.com",
                        "appid": "wx286b93c14bbf93aa",
                        "pagepath": "pages/lunar/index"
                    },
                    {
                        "type": "click",
                        "name": "赞一下我们",
                        "key": "V1001_GOOD"
                    }]
            }]
    })
    return HttpResponse("ok")


    #
    # @myrobot.key_click("music")
    # def music(message):
    #     return '你点击了“今日歌曲”按钮'
