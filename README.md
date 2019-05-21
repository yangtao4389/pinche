# pinche
pinche web service


#### 各个页面接口：
##### 拼车app：
http://127.0.0.1:8000/carPooling/Home/   首页
http://127.0.0.1:8000/carPooling/GetCityList/   POST  获取城市列表



 
 
##### 表设计逻辑，以行程为中心单位，进行必要的其余表设计



#### 框架逻辑
进入的时候会进行用户信息验证
微信相关的逻辑全部用wxbackend来处理
拼车主要业务通过carPooling
weixinLibrary 是引用的https://github.com/zwczou/weixin-python



---- 修改框架2019-05-11
+ 中心控制端  app_center   移植原先的centerEvent
+ 对接微信端  app_weixin   移植原先的wxbackend
+ 对接拼车端  app_carpool  依旧用原先的carPooling
+ 其它业务    app_


+ 辅助工具(不涉及到创建表的)    tools/
+ 其它第三方库（需要改源码的）   py_modules

+ 入口路径：django_app








#### py_modules
用于使用第三方库，比方xadmin这种存在很多bug的库
先将py_modules 加入到系统路径
import sys
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'py_modules'))  # 防止某些库是自己引用自己
引入的话，全局统一：from py_modules..... import ..


---- 引用第三方库werobot安装包：
xmltodict




#### app_weixin
+ 服务器配置验证(返回信息数据处理) 
+ 菜单创建
----该接口必须手动调用

#### app_carpool
+ 权限过滤，当访问webApp下面的url的时候，必须登录
    登录页面再处理一下，说白了必须绑定手机



#### carPooling
主要用于页面展示



#### eventNotice 
+ 用于调用发送短信接口