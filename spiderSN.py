import asyncio
import json
import re
import time
from lxml import etree
import datetime
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker
import SQLModule
import isHoliday
from SQLModule import engine


class spiderSuNing():
    def __init__(self, keyword,Session_class):
        self.keyword = keyword
        self.sesstion = Session_class()
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

    async def get_speci(self, url):  # specification
        resp = await self.my_request(method='GET', url=url, headers=self.headers)
        try:
            text = re.findall('更多参数</a></span> </div> (.*?</ul>) </div>', resp.text)[0]
        except IndexError:
            print("苏宁易购采集完成")
            return None
        html = etree.HTML(text)
        speci = html.xpath("//text()")
        speci = [i for i in speci if i != " "]
        return speci

    async def getinfo(self):
        url = 'https://search.suning.com/{}/'.format(self.keyword)
        resp = await self.my_request(method='GET', url=url, headers=self.headers)
        await self.parse(resp)
        for j in range(2, 6):
            data = {
                'keyword': self.keyword,
                'ci': 0,
                'pg': j,
                'yjhx': '',
                'cp': 0,
                'il': 0,
                'st': 0,
                'iy': 0,
                'isNoResult': 0,
                'n': 1,
                'sesab': 'ACAABBABCAAA',
                'id': 'IDENTIFYING',
                'cc': 853,
                'paging': 2,
                'sub': 0,
                'jzq': 15833,
            }
            nexturl = 'https://search.suning.com/emall/searchV1Product.do'
            resp = await self.my_request(method='GET', url=url, headers=self.headers, params=data)
            status = await self.parse(resp)
            if status == None:
                break
        await asyncio.sleep(1)
        await self.AsyncSession.aclose()

    async def parse(self, resp):
        html = etree.HTML(resp.text)
        html = html.xpath('//ul[contains(@class,"general")]/li')
        for i in html:
            product = i.xpath(".//div[@class='title-selling-point']")[0]
            title = ''.join(product.xpath(".//text()")).replace("\n", "")
            source_url = 'https:' + str(product.xpath("./a[1]/@href")[0])
            img_url = 'https:' + str(i.xpath(".//img/@src")[0])
            newurl = 'https://ds.suning.com/ds/generalForTile/{}-853-2-0000000000-1--.jsonp'.format(
                "0000000" + source_url.split("/")[-1].split(".")[0])
            info = await self.my_request(method='GET', url=newurl, headers=self.headers)
            info = json.loads(info.text.strip(';').strip("(").strip(")"))['rs'][0]
            current_price = info['price']
            stock = info['promotionLable']
            if stock != '预约':
                stock = '有货'
            try:
                discount = info['promotionList']['simple']
            except:
                discount = "无"
            if not discount:
                discount = '无'
            site_source = '苏宁易购'
            specification = await self.get_speci(source_url)
            if specification == None:
                return None
            if len(specification) == 11:
                shop_name = await self.parse_detail(source_url)
                if not current_price:
                    current_price = await self.get_price("0000000" + source_url.split("/")[-1].split(".")[0])
                brand_name = specification[1]
                model = specification[5].split("：")[1].replace(" ","")
                chip_brand = specification[4].split("：")[1]
                graphics_type = specification[7].split("：")[1]
                graphics_memory = specification[8].split("：")[1]
                if '及以上' in graphics_memory:
                    continue
                fan_count = specification[-1].split("：")[1]
                datenow=datetime.datetime.now().strftime("%Y-%m-%d")
                isholiday=isHoliday.isholiday(datenow[5:])
                if model=="其他":
                    model = await self.parse_model(specification[2].split("：")[1].replace(" ",""))
                    if model==False:
                        continue
                tb = SQLModule.CommodityInfo(title=title,source_url=source_url,img_url=img_url,current_price=current_price,stock=stock,discount=discount
                                             ,site_source=site_source,brand_name=brand_name,model=model.upper(),chip_brand=chip_brand,graphics_type=graphics_type
                                             ,graphics_memory=graphics_memory,fan_count=fan_count,shop_name=shop_name,date=datenow,is_holiday=isholiday)
                self.sesstion.add(tb)
                self.sesstion.commit()

    async def parse_model(self,model):
        finally_model=re.findall('[RGTX]+\d{3,4}[XTSuperUPERi]+',model)
        if len(finally_model)<1:
            finally_model=re.findall('[TITANtitan]{5}',model)
            if finally_model=='GTXTITAN':
                finally_model='TITAN'
            if len(finally_model)<1:
                return False
            else:
                return finally_model[0].upper()
        else:
            return finally_model[0].upper()

    async def get_price(self, sku):
        url = 'https://pas.suning.com/nspcsale_0_{}_{}_0070175526_220_853_8530199_157122_1000078_9078_10534_Z001___R1506003_2.0_1___000056750____0___2000.0_2__20529_186002__.html?callback=pcData&_={}'.format(
            sku, sku, int(time.time() * 1000))
        url2 = 'https://pas.suning.com/nspcsale_0_{}_{}_0070070272_220_853_8530199_157122_1000078_9078_10534_Z001___R1506003_1.5_1___000056750____0___887.11_2__20529_186002__.html?callback=pcData&_={}'.format(
            sku, sku, int(time.time() * 1000))
        url3 = 'https://pas.suning.com/nspcsale_0_{}_{}_0070172882_220_853_8530199_157122_1000078_9078_10534_Z001___R1506003_0.8_1___000050860____0___300.0_2__20529_186002__.html?callback=pcData&_={}'.format(
            sku, sku, int(time.time() * 1000))
        url4 = 'https://pas.suning.com/nspcsale_0_{}_{}_0070143867_220_853_8530199_157122_1000078_9078_10534_Z001___R1506003_2.445_1___000050860____0___2688.0_2__20529_186002__.html?callback=pcData&_={}'.format(
            sku, sku, int(time.time() * 1000))
        url5 = 'https://pas.suning.com/nspcsale_0_{}_{}_0071153419_220_853_8530199_157122_1000078_9078_10534_Z001___R1506003_0.02_3___0000572X9_01___0___0.02_2__20529_186002__.html?callback=pcData&_={}'.format(
            sku, sku, int(time.time() * 1000))
        resp = await self.my_request(method='GET', url=url, headers=self.headers)
        resp = json.loads(resp.text.strip("pcData(")[:-2])
        price = resp['data']['price']['saleInfo'][0]['netPrice']
        if not price:
            resp = await self.my_request(method='GET', url=url2, headers=self.headers)
            resp = json.loads(resp.text.strip("pcData(")[:-2])
            price = resp['data']['price']['saleInfo'][0]['netPrice']
            if not price:
                resp = await self.my_request(method='GET', url=url3, headers=self.headers)
                resp = json.loads(resp.text.strip("pcData(")[:-2])
                price = resp['data']['price']['saleInfo'][0]['netPrice']
                if not price:
                    resp = await self.my_request(method='GET', url=url4, headers=self.headers)
                    resp = json.loads(resp.text.strip("pcData(")[:-2])
                    price = resp['data']['price']['saleInfo'][0]['netPrice']
                    if not price:
                        resp = await self.my_request(method='GET', url=url5, headers=self.headers)
                        resp = json.loads(resp.text.strip("pcData(")[:-2])
                        price = resp['data']['price']['saleInfo'][0]['netPrice']
        return price

    async def parse_detail(self, url):
        resp = await self.my_request(method='GET', url=url, headers=self.headers)
        try:
            title = re.findall('<title>(.*?)</title>', resp.text)[0].split('-苏宁易购')[1]
        except Exception as e:
            print(e)
        return title


def run(keyword):
    Session_class = sessionmaker(bind=engine)
    s = spiderSuNing(keyword,Session_class)
    asyncio.run(s.getinfo())


if __name__ == '__main__':
    run('显卡')
