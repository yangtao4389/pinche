"""sichuan_yd_video URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include,re_path
from django.conf.urls import url

from carPooling import views,api_home,error,api_userass,api_account,api_userrec,msg_polling

# msg_polling.runserver_from_start()

# 静态页面
urlpatterns = [
    url(r"^Home$", views.Home),
    url(r"^Home/Index$", views.Home),  #首页
    url(r"^Home/Login$", views.Login),  # 登录
    url(r"^Home/WeixinLogin$", views.WeixinLogin,name="WeixinLogin"),  # 微信登录
    url(r"^Home/WeiXinLoginCallBack$", views.WeiXinLoginCallBack,name="WeiXinLoginCallBack"),  # 微信登录后的回调
    url(r"^Home/WeiXinSubscrible$", views.WeiXinSubscrible),  # 微信登录后的回调

    url(r"^Home/AssList$", views.AssList),  # 行程列表
    url(r"^Home/AssShareTip$", views.AssShareTip),  # 分享行程

    url(r"^UserAss/Publish$", views.UserAssPublish),  # 发布行程
    url(r"^UserAss/Detail", views.UserAssDetail),  # 车主行程详情
    url(r"^UserAss/Edit$", views.UserAssEdit),  # 车主行程编辑

    url(r"^UserAss/List$", views.UserAssList),   #  我的行程列表  我是车主

    url(r"^UserRec/List$", views.UserRecList),  #  我的行程列表  我是乘客
    url(r"^UserRec/Detail$", views.UserRecDetail),  #  我的行程  我是乘客 预订详情



    url(r"^UserCenter$", views.UserCenter),  #  个人中心
    url(r"^UserCenter/ChangePhone$", views.UserCenterChangePhone),  #  关于电话的绑定与修改地址
    url(r"^UserCenter/DalanceLogList$", views.UserCenterDalanceLogList),  #  关于电话的绑定与修改地址

    url(r"^About$", views.About),  #  乘车协议
    url(r"^About/CreditValueNote$", views.AboutCreditValueNote),  #  诚信值信息


]

# ajax请求



urlpatterns += [
    url(r"^Home/GetCityList$", api_home.GetCityList),
    url(r"^Home/GetHotLine$", api_home.GetHotLine),
    url(r"^Home/GetCurTripTip$", api_home.GetCurTripTip),
    url(r"^Home/GetAssList$", api_home.GetAssList),
    url(r"^Home/GetWenxinJsapiConfig$", api_home.GetWenxinJsapiConfig),
    url(r"^Home/CheckWeiXinSubscribe$", api_home.CheckWeiXinSubscribe),
]

# 车主
urlpatterns += [
    url(r"^UserAss/GetDetailData$", api_userass.GetDetailData), # 获取通用数据 不进行任何判断
    url(r"^UserAss/GetRecListByAss$", api_userass.GetRecListByAss), # 获取通用数据 不进行任何判断

    url(r"^UserAss/SavePublish$", api_userass.SavePublish),  # 保存
    url(r"^UserAss/GetLastAss$", api_userass.GetLastAss),  # 获取上一次的发布数据
    url(r"^UserAss/Cancel$", api_userass.Cancel),  # 取消
    url(r"^UserAss/noLeftSeat$", api_userass.noLeftSeat),  # 设为无座
    # url(r"^UserAss/SaveEdit$", api_userass.SaveEdit),  # 保存
    url(r"^UserAss/GetList$", api_userass.GetList),  # 保存
    url(r"^UserAss/Del$", api_userass.Del),  # 保存
]

# 乘客
urlpatterns += [
    url(r"^UserRec/SaveBook$", api_userrec.SaveBook),  # 乘客订座接口
    url(r"^UserRec/GetList$", api_userrec.GetList),  # 乘客订座接口
    url(r"^UserRec/GetDetailData$", api_userrec.GetDetailData),  # 获取通用数据
    url(r"^UserRec/Del$", api_userrec.Del),  # 获取通用数据
    url(r"^UserRec/UnbookSave$", api_userrec.UnbookSave),  # 获取通用数据

]



urlpatterns += [
    url(r"^UserCenter/GetPhoneStatus$", api_account.PhoneStatus),  # 保存
    # url(r"^UserCenter/GetVerifyCodeImg", api_account.GetVerifyCodeImg),  # 获取手机验证图片
    url(r"^UserCenter/GetUserInfo$", api_account.GetUserInfo),  # 获取用户信息，全局用
    url(r"^UserCenter/GetCodeLogin$", api_account.GetCodeLogin),  # 获取用户信息，全局用
    # url(r"^UserCenter/SaveChangePhone$", api_account.SaveChangePhone),  # 保存号码跟用户真实姓名
    url(r"^UserCenter/GetDalanceLogList$", api_account.GetDalanceLogList),  # 获取用户交易信息
]


# 错误信息
urlpatterns += [
    url(r"^Error/JsError$", error.JsError),
]

# 轮询进行通知 两分钟一次
urlpatterns += [
    url(r"^lunxun/msg_polling$", msg_polling.runserver_from_start),
]

