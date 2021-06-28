import asyncio
from lxml import etree
from sqlalchemy.orm import sessionmaker
from SQLModule import engine, commodities
from httpx import AsyncClient
from proxy import MySession
import datetime
class spiderJingDong():
    def __init__(self, keyword):
        Session_class = sessionmaker(bind=engine)
        self.keyword = keyword
        DBSession =sessionmaker(bind=engine)
        self.session = DBSession()
        self.AsyncSession = MySession()  # 代理
        # self.AsyncSession = AsyncClient()  # 本地
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'}

    async def my_request(self, method='GET', url=None, headers=None, params=None, json=None, files=None, data=None,
                         allow_redirects=True, timeout=10):
        for _ in range(5):
            try:
                resp = await self.AsyncSession.request(method=method, url=url, headers=headers, params=params,
                                                       data=data, allow_redirects=allow_redirects, json=json,
                                                       files=files,
                                                       timeout=timeout)
                return resp
            except Exception as e:
                print(e)

    async def run(self):
        url = 'https://search.jd.com/search.php'
        datas = {
            'keyword': self.keyword,
            'page': 1,
        }
        # print("start crawl...")
        await self.parse_html(url,datas)
        await asyncio.sleep(1)
        await self.AsyncSession.aclose()

    async def parse_html(self, url, datas):
        resp = await self.my_request(method='GET', url=url,params=datas, headers=self.headers)
        html = etree.HTML(resp.text)
        max_page = int(''.join(''.join(html.xpath("//span[@class='fp-text']//text()")).split()).split("/")[1])
        for i in range(1, max_page + 1):
            # print(i)
            datas['page']=i
            newurl = url + '&page=' + str(i)
            resp = await self.my_request(method='GET', url=newurl, params=datas,headers=self.headers)
            html = etree.HTML(resp.text)
            goods_list = html.xpath("//div[@id='J_goodsList']/ul/li")
            commodity={}
            for j in goods_list:
                #'/html/body/*[not(name()="span")]//text()')
                tag=j.xpath(".//div[contains(@class,'p-name')]/a/em/span[@class='p-tag']/text()")[0] if j.xpath(".//div[contains(@class,'p-name')]/a/em/span[@class='p-tag']") else ""
                commodity['title']=''.join(j.xpath(".//div[contains(@class,'p-name')]/a/em//text()")).replace(tag,"").strip()
                commodity['source_url'] = "https:"+j.xpath(".//div[@class='p-img']/a/@href")[0]
                commodity['current_price'] = j.xpath(".//div[@class='p-price']//i/text()")[0]
                commodity['img_url'] = "https://"+j.xpath(".//div[@class='p-img']/a/img/@data-lazy-img")[0].strip("//")
                try:
                    commodity['shop_name'] = j.xpath(".//div[@class='p-shop']//a/@title")[0]
                except IndexError:
                    commodity['shop_name'] = ""
                commodity['site_source']= "京东自营" if '自营' in j.xpath(".//div[@class='p-icons']/i/text()") else "京东"
                # print(commodity)
                await self.addDb(commodity)


    async def addDb(self, commodity):
        c = self.session.query(commodities).filter_by(source_url=commodity['source_url']).first()
        if c == None:
            com = commodities(title=commodity['title'],
                              current_price=commodity['current_price'],
                              promotion_price=commodity['current_price'],
                              img_url=commodity['img_url'],
                              source_url=commodity['source_url'],
                              site_source=commodity['site_source'],
                              shop_name=commodity['shop_name'],
                              date=datetime.datetime.now())
            # print(com.title)
            self.session.add(com)
            self.session.commit()
        else:
            c: commodities
            c.title = commodity['title'],
            c.current_price = commodity['current_price'],
            c.promotion_price = commodity['current_price'],
            c.img_url = commodity['img_url'],
            c.source_url = commodity['source_url'],
            c.site_source = commodity['site_source'],
            c.shop_name = commodity['shop_name'],
            c.date = datetime.datetime.now()
            self.session.commit()


if __name__ == '__main__':
    s = spiderJingDong('显卡')
    asyncio.run(s.run())
