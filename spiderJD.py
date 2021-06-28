import asyncio
import datetime
from lxml import etree
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

import isHoliday, SQLModule
from SQLModule import engine
from proxy import MySession

class JingDong():
    def __init__(self, Session_class):
        self.AsyncSession = AsyncClient()

        self.sesstion = Session_class()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
            'Cookie': 'shshshfpa=6478005c-94e3-278d-fe3d-b6fe21051e46-1600934185; shshshfpb=gV7e7qmtgcNmSrPHBk%2FTMyA%3D%3D; __jdu=1623221479805637799421; unpl=V2_ZzNtbUVSERVzXUJSLEldA2JWFV1LVxATdwtEUXpLXVFuURJcclRCFnUUR1NnGFQUZwcZXEZcQhRFCEdkcxFUDGcKGm0AAkIlRQtGZHopXAJkARFeQlJFHXwJQlN5H1oNbwYRXXJnQx1xOEZVehpbBG8GFFlDVUodRd3P5aKd2tLVkiJVSl9KFX0LdlVLG10EZwUVVEReRiU0ZkZVfxhcDWQGX11FVEEWdghDUnMQXQFgARRbSl9GFnU4R2R4; qrsc=3; areaId=24; PCSYCityID=CN_520000_520400_520424; user-key=c191c23b-804c-4542-af9b-1083abe32748; _pst=jd_6c575a7b0c2f0; unick=jd_6c575a7b0c2f0; pin=jd_6c575a7b0c2f0; _tp=6Jcu529z3%2BtOHLmKhsSCSfDMZw8arJ25w43rmu91GKE%3D; pinId=ZnockAvXCu7A3IGRIYeZLbV9-x-f3wj7; __jdv=122270672|direct|-|none|-|1624518348194; ipLoc-djd=24-2189-2190-58239; __jdc=122270672; shshshfp=8db867539aa329f145c434563c19f51e; rkv=1.0; wlfstk_smdl=xjbmx9h29vjjueepjdi13mx0w47chw6e; TrackID=18Sil1DqmWsYi_I2WY48jA9uB8VZxMc60TnBWNSoFtLfRV9-x_cybr--6HCq0h8z0houL2G-LRbF25QgfNa8vZ-loPbaxbHkqjmcV2t15q0xPGK8jtwhY9Bvyqnofr2sg; ceshi3.com=000; __jda=122270672.1623221479805637799421.1623221480.1624513834.1624525916.19; thor=20AE5F9AAF50072E0C5C1AE5522C7C4952E806911481F243C2214AF620F69BF28D0B1DD44F00705975BA900C1946DFD5164178F3FBB8120A939539DC2B5D51845A7B1E16AA821704F18BF5F986D521A169DBE3CBD6F7955DDC308398B693DA5519A5FC822B2848CB9B566A5271755B223C79F0181D0D9C406F19A0693E94D8B832E41E7572EA6998691D37443F9733BB56A9AE20730141CB04F040C6B071883D; shshshsID=cbb19f7e3d257785e594a2cb2c6f28cb_7_1624527359017; __jdb=122270672.7.1623221479805637799421|19.1624525916; 3AB9D23F7A4B3C9B=J2TJ67KMZAIXCMIJ6RCCN54PHFMX5HTIC5BEB5RDJ4WPE4AZDHOASILUJT5WHZMEJU44AXHMZGEYFDS4XW2GCRNVSU'}

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
                pass

    async def getItems(self):
        url = 'https://search.jd.com/Search?keyword=%E6%98%BE%E5%8D%A1&enc=utf-8&wq=%E6%98%BE%E5%8D%A1'
        resp = await self.my_request(url=url, headers=self.headers)
        html = etree.HTML(resp.text)
        lis = html.xpath('//li[@data-group="0"]')
        resa = {}
        for li in lis:
            resa[li.xpath('.//a/text()')[0]] = 'https://search.jd.com/' + li.xpath('.//a/@href')[0]
        return resa

    async def getTextInfo(self, id):
        url = 'https://item.jd.com/{}.html'.format(id)
        resp = await self.my_request(url=url, headers=self.headers)
        html = etree.HTML(resp.text)
        speci = html.xpath("//ul[contains(@class,'p-parameter-list')]/li")
        # print(resp.text)
        if len(speci) < 1:
            await self.getTextInfo(id)
        else:
            specifications = await self.get_speci(speci)
            specifications['source_url'] = url
            return specifications

    async def get_speci(self, speci):
        self.specifications = {}
        self.specifications["chip_brand"] = '其他'
        self.specifications["fan_count"] = '其他'
        self.specifications["graphics_memory"] = '其他'
        self.specifications["graphics_type"] = '其他'
        for i in speci:
            text = ''.join(i.xpath(".//text()")).replace("\n", "").replace(" ", "")
            if '商品名称' in text:
                self.specifications["title"] = text.split("：")[1]
            if '品牌' in text:
                self.specifications["brand_name"] = text.split("：")[1]
            if '芯片组' in text:
                self.specifications["chip_brand"] = text.split("：")[1].replace("芯片", "")
            if '显存容量' in text:
                self.specifications["graphics_memory"] = text.split("：")[1]
            if '显存类型' in text:
                self.specifications["graphics_type"] = text.split("：")[1]
            if '散热风扇' in text:
                self.specifications["fan_count"] = text.split("：")[1]
        return self.specifications

    async def getInfo(self, url, model):
        model = model.upper().replace("TL", "TI").replace(" ", "").replace("(", "").replace(")", "")
        self.AsyncSession = MySession()
        resp = await self.my_request(url=url, headers=self.headers)
        html = etree.HTML(resp.text)
        lis = html.xpath('//div[@id="J_goodsList"]/ul/li')
        for li in lis:
            try:
                title = ''.join(li.xpath(".//div[contains(@class,'p-name')]//em//text()")).strip()
                if "整机" in title:
                    continue
                await self.AsyncSession.aclose()
                img_url = 'http:' + li.xpath('.//img//@data-lazy-img')[0]
                current_price = li.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
                shop_name = li.xpath('.//span[@class="J_im_icon"]/a/text()')[0]
                site_source = "京东"
                datenow = datetime.datetime.now().strftime("%Y-%m-%d")
                isholiday = isHoliday.isholiday(datenow[5:])
                specifications = await self.getTextInfo(li.xpath('./@data-sku')[0])
                title = self.specifications['title']
                if '其他' in self.specifications.values(): continue
                # print(title)
                # print(specifications)
                self.specifications = specifications
                tb = SQLModule.CommodityInfo(title=title, source_url=self.specifications['source_url'], img_url=img_url,
                                             current_price=current_price, stock='有货', discount='无'
                                             , site_source=site_source, brand_name=self.specifications['brand_name'],
                                             model=model, chip_brand=self.specifications['chip_brand'],
                                             graphics_type=self.specifications['graphics_type']
                                             , graphics_memory=self.specifications['graphics_memory'],
                                             fan_count=self.specifications['fan_count'],
                                             shop_name=shop_name, date=datenow, is_holiday=isholiday)
                self.sesstion.add(tb)
                self.sesstion.commit()
            except Exception as e:
                print(e)

    async def jingdong_run(self):
        items = await self.getItems()
        for key in items.keys():
            print('开始获取%s' % key)
            await self.AsyncSession.aclose()
            await self.getInfo(items[key], key)
        await self.AsyncSession.aclose()


if __name__ == '__main__':
    Session_class = sessionmaker(bind=engine)
    j = JingDong(Session_class)
    asyncio.run(j.jingdong_run())
