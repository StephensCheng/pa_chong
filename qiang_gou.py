from threading import Timer
import requests
import datetime
import demjson
import time
import json


class JD:
    headers = {
        "referer": "",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36"
    }

    def __init__(self):
        self.index = "https://www.jd.com/"
        self.user_url = "https://st.jingxi.com/_async_cookie.html?_t=1&_fromiframe=1"  # 检测用户信息
        self.buy_url = 'https://cart.jd.com/gate.action?pid={}&pcount=1&ptype=1'  # 添加到购物车
        self.pay_url = 'https://cart.jd.com/gotoOrder.action'  # 提交订单
        self.pay_success = 'https://trade.jd.com/shopping/order/submitOrder.action'  # 付款页面
        self.goods_id = "100010793471"  # 默认为R9000x的商品ID
        self.thor = "thor=F01434D8986DBF4E017D2C99C442E42465D57139EC177478C4F8C9145645A30EAEEE989A38F3F6BBE44DF5ECE456C90F48BD0DD162C6A307CAB9BBC5936FC207B544B8497CA355D643B18A4892261AD988491D2E614FC810ABDEAEE18B532A9AF2F1B62582789644947F99B9E526C97B01F503FD6F2D7C4AC5329E755BBAD3D475B8C1029BBE095A9577A973B87EB5104C21BBAD1C635DE4DE4E60BB25E3B1A5; pin=jd_7a829fe6d9093; unick=crd2018"
        self.session = requests.Session()

    def login(self, times):
        JD.headers["referer"] = "https://cart.jd.com/cart.action"
        c = requests.cookies.RequestsCookieJar()
        c.set("thor", self.thor)
        self.session.cookies.update(c)
        response = self.session.get(
            url=self.user_url, headers=JD.headers).text.strip("jsonpUserinfo()\n")
        response = demjson.encode(response, encoding="utf-8")
        user_info = json.loads(response)

        print("账号：", user_info.get("unick"))

        if user_info.get("unick"):
            self.shopping(times)


def shopping(self, times):
    # 输入商品链接获取商品的ID
    goods_url = input("请输入商品链接：")
    self.goods_id = goods_url[goods_url.rindex("/") + 1:goods_url.rindex(".")]
    JD.headers["referer"] = goods_url
    buy_url = self.buy_url.format(self.goods_id)
    while True:
        now = datetime.datetime.now()
        if now > times:
            self.session.get(url=buy_url, headers=JD.headers)
            self.session.get(url=self.pay_url, headers=JD.headers)
            response = self.session.post(
                url=self.pay_success, headers=JD.headers
            )
            order_id = json.loads(response.text).get("orderID")
            if order_id:
                print("抢购成功，订单号：", order_id)


if __name__ == '__main__':
    set_time = datetime.datetime(2021, 4, 3, 15, 38)
    jd = JD()
    jd.login(times=set_time)
