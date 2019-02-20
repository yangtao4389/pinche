'''
统一定义返回json数据的格式
'''
import json

class RtnCode():
    # 正常返回
    STATUS_OK = "200"
    # 参数错误
    STATUS_PARAM = "001"
    # 接口未发现
    STATUS_NOFOUND = "404"
    # 服务器出错
    STATUS_SYSERROR = "500"

class RtnDefault():
    '''
    默认返回信息
    '''
    def __init__(self,Status,Message=None,Data=None):
        self.Status = Status
        self.Message = Message
        self.Data = Data

    def __str__(self):
        return json.dumps(dict(
            statusCode=self.Status,
            message=self.Message,
            data=self.Data,
        ))



if __name__ == '__main__':
    a = RtnDefault(RtnCode.STATUS_OK,"ok")
    print(a)