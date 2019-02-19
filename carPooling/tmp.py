import requests

if __name__ == '__main__':
    # url = "http://lw.51bc.cc/WebApp/UserAss/Publish"
    url = "http://lw.51bc.cc/WebApp/UserCenter"
    url = "http://lw.51bc.cc/WebApp/Home/GetWenxinJsapiConfig"
    url = "http://lw.51bc.cc/WebApp/UserAss/SavePublish"
    url = "http://lw.51bc.cc/WebApp/Home/AssShareTip?id=b8cf77a3-c671-4560-9bed-a746b8a52276"
    url = "http://lw.51bc.cc/WebApp/UserAss/Detail?id=b8cf77a3-c671-4560-9bed-a746b8a52276"
    url = "http://lw.51bc.cc/WebApp/UserAss/Edit?id=b8cf77a3-c671-4560-9bed-a746b8a52276"
    url = "http://lw.51bc.cc/WebApp/UserAss/Cancel"  #{"statusCode":200,"message":"操作成功!","data":null}  取消行程
    url = "http://lw.51bc.cc/WebApp/UserAss/List"  # 我的所有行程  静态页面
    # url = "http://lw.51bc.cc/WebApp/UserAss/GetList"  # 我的所有行程  post请求 {"DataSource":[{"Id":"b8cf77a3-c671-4560-9bed-a746b8a52276","StartCity":"成都","EndCity":"巴中","GoTime":"2019/2/20 0:00:00","BusType":"丰田致炫","Seat":3,"BookedSeat":0,"Status":0},{"Id":"98df873c-61a1-45dd-82e5-a1d5474bd898","StartCity":"巴中","EndCity":"成都","GoTime":"2018/5/1 12:00:00","BusType":"丰田致炫","Seat":0,"BookedSeat":2,"Status":1},{"Id":"d5afae95-72ca-43b3-8fef-b1bcea75fc08","StartCity":"成都","EndCity":"巴中","GoTime":"2018/4/29 8:00:00","BusType":"丰田致炫","Seat":0,"BookedSeat":3,"Status":1}],"CurrentPageIndex":1,"PageSize":20,"RowCount":3,"PageCount":1,"IsFirstPage":true,"IsLastPage":true,"CurrentRowCount":3,"CurrentStartIndex":1,"CurrentEndIndex":3,"DataSource":[{"Id":"b8cf77a3-c671-4560-9bed-a746b8a52276","StartCity":"成都","EndCity":"巴中","GoTime":"2019/2/20 0:00:00","BusType":"丰田致炫","Seat":3,"BookedSeat":0,"Status":0},{"Id":"98df873c-61a1-45dd-82e5-a1d5474bd898","StartCity":"巴中","EndCity":"成都","GoTime":"2018/5/1 12:00:00","BusType":"丰田致炫","Seat":0,"BookedSeat":2,"Status":1},{"Id":"d5afae95-72ca-43b3-8fef-b1bcea75fc08","StartCity":"成都","EndCity":"巴中","GoTime":"2018/4/29 8:00:00","BusType":"丰田致炫","Seat":0,"BookedSeat":3,"Status":1}]}
    url = "http://lw.51bc.cc/WebApp/UserAss/GetList"  # 车主
    url = "http://lw.51bc.cc/WebApp/UserRec/GetList"  # 乘客
    url = "http://lw.51bc.cc/WebApp/UserRec/SubscribeList"  # 我的预约
    url = "http://lw.51bc.cc/WebApp/UserRec/Subscribe?id=638981b3-aeb6-4a4a-8e31-70e3e7a3a3b4"  # 编辑预约
    url = "http://lw.51bc.cc/WebApp/UserCenter/ChangePhone"  # 修改手机号
    url = "http://lw.51bc.cc/WebApp/UserAuth/RealName"  # 实名认证
    url = "http://lw.51bc.cc/WebApp/UserAuth/RealDriver"  # 车主认证
    url = "http://lw.51bc.cc/WebApp/Home"
    url = "http://lw.51bc.cc/WebApp/UserAss/GetDetailData"
    headers = {
        "Cookie":"Hm_lpvt_a0694c9c6c17b1bfb616beb7d946aecb=1550479570; Hm_lvt_a0694c9c6c17b1bfb616beb7d946aecb=1549698174,1549778423,1550138143,1550479419; xmq_UserCookie=openid=026DAD83B73A6137D0E5B1BD3EAE1CED6CA04AD6C3D9115FCB7FE96E2EEB071E; ASP.NET_SessionId=aapdovmtcaxjvbbxuw50las1"
    }
    response = requests.post(url=url,headers=headers)
    content = response.text
    print(content)
    with open("aa.html",'w',encoding="utf-8") as f:
        f.write(content)