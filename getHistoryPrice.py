import asyncio
from sqlalchemy.orm import sessionmaker
from SQLModule import engine
from SQLModule import CommodityInfo
from proxy import MySession


class getHistory:
    def __init__(self,id,session):
        self.session=session
        self.AsyncSession = MySession()  # 代理
        # self.AsyncSession = AsyncClient()  # 本地
        self.source_url=id
        self.id = self.raw(id)
        self.headers = {
        'Host': 'apapia.manmanbuy.com',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Proxy-Connection': 'close',
        'Cookie': 'ASP.NET_SessionId=yh0pkbngkptssqspybzteb20; jjkcpnew111=cp46144734_1171363291_2017/11/25',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_3 like Mac OS X) AppleWebKit/603.3.8 (KHTML, like Gecko) Mobile/14G60 mmbWebBrowse',
        # 'Content-Length': '457',
        'Accept-Encoding': 'gzip',
        'Connection': 'close'}
        self.postdata = 'c_devid=2C5039AF-99D0-4800-BC36-DEB3654D202C&username=&qs=true&c_engver=1.2.35&c_devtoken=&c_devmodel=iPhone%20SE&c_contype=wifi&' \
                   't=1537348981671&c_win=w_320_h_568&p_url={}&' \
                   'c_ostype=ios&jsoncallback=%3F&c_ctrl=w_search_trend0_f_content&methodName=getBiJiaInfo_wxsmall&c_devtype=phone&' \
                   'jgzspic=no&c_operator=%E4%B8%AD%E5%9B%BD%E7%A7%BB%E5%8A%A8&c_appver=2.9.0&bj=false&c_dp=2&c_osver=10.3.3'.format(
            self.id)
        self.AsyncSession.headers.update(self.headers)

    def raw(self,text):  # 转化URL字符串
        escape_dict = {
            '/': '%252F',
            '?': '%253F',
            '=': '%253D',
            ':': '%253A',
            '&': '%26'}
        new_string = ''
        for char in text:
            try:
                new_string += escape_dict[char]
            except KeyError:
                new_string += char
        return new_string

    async def my_request(self, method='GET', url=None, headers=None, params=None,json=None, files=None,data=None, allow_redirects=True,timeout=10):
        for _ in range(5):
            try:
                resp = await self.AsyncSession.request(method=method, url=url, headers=headers, params=params,
                                                   data=data, allow_redirects=allow_redirects, json=json, files=files,
                                                   timeout=timeout)
                return resp
            except Exception as e:
                print("错误："+str(e))
                pass

    async def getinfo(self):
        while True:
            try:
                url = 'https://apapia.manmanbuy.com/ChromeWidgetServices/WidgetServices.ashx'
                req = await self.my_request(method='GET',url=url, data=self.postdata,headers=self.headers)
                try:
                    req=req.json()['single']
                except:
                    print(req.text)
                title=req['title']
                currentPrice=req['spmoney']
                smallPic=req['smallpic']
                bigPic=req['bigpic']
                history=req['jiagequshi']
                source=req['zk_scname']
                url=req['url']
                # print(self.source_url)
                # print(history)
                c=self.session.query(CommodityInfo).filter_by(source_url=self.source_url).first()
                c.history_price=history
                print(c.id)
                self.session.commit()
                break
            except:
                return None
        # 'lowerPrice': 369.0, 'lowerPriceyh': 332.1, 'currentPriceStatus': '近期价格上涨', 'currentPriceyhStatus': '低于30天平均', 'lowerDate': '/Date(1591027200000+0800)/', 'lowerDateyh': '/Date(1591027200000+0800)/', 'bj': [], 'qushi': '上涨',

    async def run(self):
        await self.getinfo()
        await asyncio.sleep(1)
        await self.AsyncSession.aclose()

def run():
    Session_class = sessionmaker(bind=engine)
    session = Session_class()
    all_data = session.query(CommodityInfo).filter_by().all()
    for i in all_data:
        if not i.history_price:
            history=getHistory(i.source_url,session)
            asyncio.run(history.run())

if __name__ == '__main__':##京东、淘宝、天猫等电商平台数据都可以获取
    run()

