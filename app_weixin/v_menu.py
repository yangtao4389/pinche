from django.shortcuts import HttpResponse

from .settings import myrobotclient, myrobot


def createMenu(request):
    myrobotclient.create_menu({
        "button": [
            {
                "type": "view",
                "name": "我要拼车",
                "url": "http://www.rhax.cn/WebApp/Home"
            },
            {
                "type": "view",
                "name": "发布行程",
                "url": "http://www.rhax.cn/WebApp/UserAss/Publish"
            },
            {
                "name": "个人中心",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "个人中心",
                        "url": "http://www.rhax.cn/WebApp/UserCenter"
                    },
                    {
                        "type": "view",  # web页面
                        "name": "更新菜单",
                        "url": "http://211.149.180.119/wxbackend/createMenu/"
                    },
                    # {
                    #     "type": "miniprogram",  # 小程序
                    #     "name": "万年历",
                    #     "url": "http://mp.weixin.qq.com",
                    #     "appid": "wx286b93c14bbf93aa",
                    #     "pagepath": "pages/lunar/index"
                    # },
                   ]
            }]
    })
    return HttpResponse("ok")


    #
    # @myrobot.key_click("music")
    # def music(message):
    #     return '你点击了“今日歌曲”按钮'
