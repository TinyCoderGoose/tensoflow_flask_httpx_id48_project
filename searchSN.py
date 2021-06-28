import asyncio
import json
from lxml import etree
import datetime
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
from SQLModule import engine, commodities


class spiderSuNing():
    def __init__(self, keyword):
        Session_class = sessionmaker(bind=engine)
        self.keyword = keyword
        self.sesstion = Session_class()
        DBSession =sessionmaker(bind=engine)
        self.session = DBSession()
        self.AsyncSession = AsyncClient()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36 Edg/91.0.864.48'}

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
        url = 'https://search.suning.com/{}/'.format(self.keyword)
        resp = await self.my_request(method='GET', url=url, headers=self.headers)
        html=etree.HTML(resp.text)
        max_page=int(html.xpath("//span[@class='fl']/em/text()")[1])
        await self.parse(resp)
        # for j in range(2, max_page):
        #     data = {
        #         'keyword': self.keyword,
        #         'ci': 0,
        #         'pg': j,
        #         'yjhx': '',
        #         'cp': 0,
        #         'il': 0,
        #         'st': 0,
        #         'iy': 0,
        #         'isNoResult': 0,
        #         'n': 1,
        #         'sesab': 'ACAABBABCAAA',
        #         'id': 'IDENTIFYING',
        #         'cc': 853,
        #         'paging': 2,
        #         'sub': 0,
        #         'jzq': 15833,
        #     }
        #     nexturl = 'https://search.suning.com/emall/searchV1Product.do'
        #     resp = await self.my_request(method='GET', url=nexturl, headers=self.headers, params=data)
        #     await self.parse(resp)
        await asyncio.sleep(1)
        await self.AsyncSession.aclose()

    async def parse(self, resp):
        html = etree.HTML(resp.text)
        html = html.xpath('//ul[contains(@class,"general")]/li')
        commodity={}
        for i in html:
            commodity['title']=i.xpath(".//div[@class='title-selling-point']/a")[0].xpath('string(.)').split("\n")[0]
            commodity['source_url']='https:'+i.xpath(".//div[@class='title-selling-point']/a/@href")[0]
            commodity['img_url']='https:'+i.xpath(".//a[@class='sellPoint']/img/@src")[0]
            commodity['shop_name']=i.xpath(".//a[@class='store-name']//text()")
            if commodity['shop_name']:
                shop_name=commodity['shop_name'][0]
            else:
                commodity['shop_name']='苏宁自营'
            commodity['site_source'] = '苏宁易购'
            newurl = 'https://ds.suning.com/ds/generalForTile/{}-853-2-{}-1--.jsonp'.format(
                "0000000" + commodity['source_url'] .split("/")[-1].split(".")[0],commodity['source_url'].split("/")[-2])
            info = await self.my_request(method='GET', url=newurl, headers=self.headers)
            info = json.loads(info.text.strip(';').strip("(").strip(")"))['rs'][0]
            commodity['current_price'] = info['snPrice']
            commodity['promotion_price']=info['arrivalPrice']
            if not commodity['promotion_price']:
                commodity['promotion_price']= info['price']
            await self.addDb(commodity)

    async def addDb(self, commodity):
        c = self.session.query(commodities).filter_by(source_url=commodity['source_url']).first()
        if c == None:
            com = commodities(title=commodity['title'],
                              current_price=commodity['current_price'],
                              promotion_price=commodity['promotion_price'],
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
    s = spiderSuNing('显卡')
    asyncio.run(s.run())
