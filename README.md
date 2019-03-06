# pinche
pinche web service


#### 各个页面接口：
##### 拼车app：
http://127.0.0.1:8000/carPooling/Home/   首页
http://127.0.0.1:8000/carPooling/GetCityList/   POST  获取城市列表



 
 
##### 表设计逻辑，以行程为中心单位，进行必要的其余表设计

#### eventNotice 响应机制
分为即时响应
定时响应（该响应程序启动时就）

这里需要通过微信后台去发送消息了。

#### 框架逻辑
进入的时候会进行用户信息验证
微信相关的逻辑全部用wxbackend来处理
拼车主要业务通过carPooling

weixinLibrary 是引用的https://github.com/zwczou/weixin-python

