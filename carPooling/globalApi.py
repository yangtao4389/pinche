import traceback
from carPooling.models import CarPoolingCity,CarPoolingAssDetail,CarPoolingRecDetail,CurTripStatus





class CurTripType():
    Ass = 3   # 车主
    Rec = 2   # 乘客
    Subscribe = 1 #预约


def commonGetCurTripTip(w_openid):
    '''
    是否有该用户当前行程的信息，如果没有或者错误，则返回-1
    :param userid:
    :return:
    '''
    # # 乘客身份查看
    try:
        recDetail = CarPoolingRecDetail.objects.filter(c_userid=w_openid).filter(status=True).filter(
            i_status__in=[CurTripStatus.Ing, CurTripStatus.Gone]).order_by("-d_go_time")
        if len(recDetail) > 0:
            assObj = recDetail[0]
            data = dict(
                result=0,
                Type=CurTripType.Rec,
                Id=assObj.c_id,
                StartCity=assObj.c_start_city,
                EndCity=assObj.c_end_city,
                GoTime=assObj.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                BookedSeat=assObj.i_booked_seat,
                redirectUrl = "/WebApp/UserRec/Detail?id=%s" %assObj.c_id,

            )
            return data
    except:
        # print(traceback.print_exc())
        data = dict(
            result=-1,
            errMsg="车主身份出错"
        )
        return data



    try:
        # 车主身份查看
        assDetail = CarPoolingAssDetail.objects.filter(c_userid=w_openid).filter(status=True).filter(i_status__in=[CurTripStatus.Ing, CurTripStatus.Gone]).order_by("-d_go_time")
        if len(assDetail)>0:
            assObj = assDetail[0]
            data = dict(
                result = 0,
                Type = CurTripType.Ass,
                Id = assObj.c_id,
                StartCity = assObj.c_start_city,
                EndCity = assObj.c_end_city,
                GoTime=assObj.d_go_time.strftime("%Y/%m/%d %H:%M:%S"),
                BookedSeat = assObj.i_booked_seat,
                Seat = assObj.i_seat,
                redirectUrl="/WebApp/UserAss/Detail?id=%s" % assObj.c_id,
            )
            return data
    except:
        # print(traceback.print_exc())
        data = dict(
            result = -1,
            errMsg = "车主身份出错"
        )
        return data

    return dict(
        result = -1,
        errMsg = "无数据"
    )