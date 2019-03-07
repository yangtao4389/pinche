from weixinLibrary import Weixin
config = dict(
    WEIXIN_APP_ID='wx7b27955ce810b11f',
    WEIXIN_APP_SECRET='d2754228e5db08f3ce1a1011d59e9798',
    WEIXIN_TOKEN="HELLOWORLD",
)
weixin = Weixin(config)



def all(**kwargs):
    return "所有没有特别定义的都返回all"

weixin.register("text","*",all)

def hello(**kwargs):
    return "hello"

weixin.register("text","hello",hello)


