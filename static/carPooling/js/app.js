var hh = {
    getLoctionHref:function () {
        var LoctionHref = location.href;
        return LoctionHref;
    },
    go: function (url) {
        //if (navigator.userAgent.toLowerCase().indexOf("ios") > 0)
        //    location.replace(url);
        //else
        location.href = url;
        try{
             event.stopPropagation();
        }catch(e){

        }
    }

    ,
    back: function (url) {
        if (history.length > 1)
            history.go(-1);
        else {
            location.href = url;
        }
         try{
             event.stopPropagation();
        }catch(e){

        }
    },
    getQueryString: function (name) {
        //获取url里的参数
        var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)","i");  //寻找&+url参数名=参数值+&.&可以不存在
        var r = window.location.search.substr(1).match(reg);
        if (r != null) return decodeURI(r[2]); return null;
    },
    pad: function (num, n) {
        //补零
        var len = num.toString().length;
        while (len < n) {
            num = "0" + num;
            len++;
        }
        return num;
    },
    isWeixin: function () {
        //是否时微信环境
        var ua = navigator.userAgent.toLowerCase();
        return ua.match(/MicroMessenger/i) == "micromessenger";
    },
    isQianfan: function () {
        //是否时微信环境
        var ua = navigator.userAgent.toLowerCase();
        return ua.match(/Qianfan/i) == "qianfan";
    },
    reload: function () {
        //微信里reload有bug
        var ua = window.navigator.userAgent.toLowerCase();
        if (ua.match(/MicroMessenger/i) == 'micromessenger') {
            location.href = location.href + (location.href.indexOf("?") > 0 ? "&" : "?") + "_=" + new Date();
        } else {
            location.reload();
        }
    },
    formatGoTime: function (goTimeStr, type) {
        if (!goTimeStr)
            return "";
        var gotime = new Date(goTimeStr);
        if (type == 1)
        {
            return gotime.Format("MM-dd hh:mm");

        }else {
            return gotime.Format("MM月dd日 hh:mm");
        }
    },
    formatTime: function (timeStr, fmt)
    {
        if (!timeStr)
            return "";
        var time = new Date(timeStr);
        return time.Format(fmt);
    },
    formatPhone: function (phone)
    {
        phone = phone.replace(/\s/g, "");
        var text_len = phone.length;
        if (text_len > 3) {

            phone = phone.substr(0, 3) + " " + phone.substr(3);
        }
        if (text_len > 8) {

            phone = phone.substr(0, 8) + " " + phone.substr(8);
        }
        return phone;
    }


};

// 对Date的扩展
//将 Date 转化为指定格式的String   
Date.prototype.Format = function (fmt) { //author: meizz   
    var o = {
        "M+": this.getMonth() + 1,                 //月份   
        "d+": this.getDate(),                    //日 
        "H+": this.getHours(),
        "h+": this.getHours(),                   //小时   
        "m+": this.getMinutes(),                 //分   
        "s+": this.getSeconds(),                 //秒   
        "q+": Math.floor((this.getMonth() + 3) / 3), //季度  
        "f": this.getMilliseconds(),             //毫秒   
        "S": this.getMilliseconds()             //毫秒   
    };
    if (/(y+)/.test(fmt))
        fmt = fmt.replace(RegExp.$1, (this.getFullYear() + "").substr(4 - RegExp.$1.length));
    for (var k in o)
        if (new RegExp("(" + k + ")").test(fmt))
            fmt = fmt.replace(RegExp.$1, (RegExp.$1.length == 1) ? (o[k]) : (("00" + o[k]).substr(("" + o[k]).length)));
    return fmt;
}
//日期 天数增减
Date.prototype.AddDay = function (days) {
    //var d = new Date(date);
    var d = this;
    d.setDate(d.getDate() + days);
    var month = d.getMonth() + 1;
    var day = d.getDate();
    if (month < 10) {
        month = "0" + month;
    }
    if (day < 10) {
        day = "0" + day;
    }
    var val = d.getFullYear() + "-" + month + "-" + day;
    return val;
}

Date.prototype.NextDay = function (days) {
    var d = this;
    d.setDate(d.getDate() + days);
    return d.getDate();
}

mui.ready(function () {
     

    ////ajax全局 加载提示
    //mui.ajaxSettings.beforeSend = function () { mui.showLoading(); };
    //mui.ajaxSettings.complete = function () { mui.hideLoading(); };
    //防劫持
    if (window.top.location.href != location.href)
        window.top.location.href = location.href;

    //安卓禁止微信放大字体
    if (typeof WeixinJSBridge == "object" && typeof WeixinJSBridge.invoke == "function") {

        handleFontSize();

    } else {
        if (document.addEventListener) {

            document.addEventListener("WeixinJSBridgeReady", handleFontSize, false);

        } else if (document.attachEvent) {

            document.attachEvent("WeixinJSBridgeReady", handleFontSize);

            document.attachEvent("onWeixinJSBridgeReady", handleFontSize);

        }
    }

    function handleFontSize() {

        // 设置网页字体为默认大小
        WeixinJSBridge.invoke('setFontSizeCallback', {

            'fontSize': 0

        });


        // 重写设置网页字体大小的事件
        WeixinJSBridge.on('menu:setfont', function () {

            WeixinJSBridge.invoke('setFontSizeCallback', {

                'fontSize': 0

            });

        });

    }

   
});

//js error log
/** 
* @param {String} errorMessage  错误信息 
* @param {String} scriptURI   出错的文件 
* @param {Long}  lineNumber   出错代码的行号 
* @param {Long}  columnNumber  出错代码的列号 
* @param {Object} errorObj    错误的详细信息，Anything 
*/
window.onerror = function (errorMessage, scriptURI, lineNumber, columnNumber, errorObj) {
    try {
        if (errorMessage.indexOf("WeixinJSBridge") == -1 && errorMessage.indexOf("SignalR") == -1 && !!scriptURI && location.href.indexOf("Location")==-1) {
            mui.post("/WebApp/Error/JsError", { msg: "url:" + location.href + "\n msg:" + errorMessage + "\n jsurl:" + scriptURI + "\n line:" + lineNumber + "\n col:" + columnNumber + "\n obj:" + errorObj }, function (json) {
                if (console)
                    console.log(json);
            });
        }
    } catch (e) {
        if (console)
            console.log(e);
    }
}
