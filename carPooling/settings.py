

# 微信接口回调域名：
WX_DOMAIN = "http://www.rhax.cn"

# 默认首页全路径
DEFAULT_HOME_FULL_PATH = "/WebApp/Home"

# 默认登录首页 如果要定义成功后的url则直接加参数为：LoginSuccessRedirectUri
DEFAULT_LOGIN_FULL_PATH = "/WebApp/Home/Login"



# 默认微信登录首页

# 微信关注页面
DEFAULT_Subscrible_FULL_PATH = "/WebApp/Home/WeiXinSubscrible"

# 默认查询该路段行程
DEFAULT_ASSLIST_FULL_PATH = WX_DOMAIN+ "/WebApp/Home/AssList?startCity=%s&endCity=%s"

# 车主
# 默认到车主出行详情
DEFAULT_UserAssDetail_FULL_PATH = WX_DOMAIN + "/WebApp/UserAss/Detail?id=%s"


# 乘客
# 默认到预定详情
DEFAULT_UserRecDetail_FULL_PATH = WX_DOMAIN+  "/WebApp/UserRec/Detail?id=%s"