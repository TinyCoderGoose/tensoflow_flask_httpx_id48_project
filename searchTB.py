import asyncio
import datetime
import hashlib
import time
from lxml import etree
from httpx import AsyncClient
from sqlalchemy.orm import sessionmaker

from SQLModule import commodities, engine


class spiderTaoBao():
    def __init__(self,name):
        self.name = name
        self.AsyncSession = AsyncClient()
        DBSession =sessionmaker(bind=engine)
        self.session = DBSession()
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54'}

    async def my_request(self, method='GET', url=None, headers=None, params=None,json=None, files=None,data=None, allow_redirects=True,timeout=10):
        for _ in range(5):
            try:
                resp = await self.AsyncSession.request(method=method, url=url, headers=headers, params=params,
                                                   data=data, allow_redirects=allow_redirects, json=json, files=files,
                                                   timeout=timeout)
                return resp
            except Exception as e:
                print(e)
                pass

    async def getSign(self,word):
        return hashlib.md5(word.encode(encoding='UTF-8')).hexdigest()

    async def getTaoBaoInfos(self,pNum,pSize):
        url ='https://h5api.m.taobao.com/h5/mtop.alimama.union.xt.en.api.entry/1.0/?'
        dataa ='{"pNum":%s'%pNum+',"pSize":"%s'%pSize+'","refpid":"mm_10011550_0_0","variableMap":"{\\"q\\":\\"%s'%self.name+'\\",\\"navigator\\":true,\\"union_lens\\":\\"recoveryid:201_11.1.99.27_4327805_1624436605241;prepvid:201_11.1.99.27_4327805_1624436605241\\",\\"recoveryId\\":\\"201_11.11.62.22_4332111_1624437603980\\"}","qieId":"34374","spm":"a2e1u.19484427.29996460","app_pvid":"201_11.11.62.22_4332111_1624437603980","ctm":"spm-url:a231o.13503973.search.1;page_url:https://ai.taobao.com/search/index.htm"}'
        datas = {
            'jsv':'2.5.1',
            'appKey':'12574478',
            't':'1624437605047',
            'sign':'56a06a51e74377be25ec10ba7511273c',
            'api':'mtop.alimama.union.xt.en.api.entry',
            'v':'1.0',
            'AntiCreep':'true',
            'timeout':'20000',
            'AntiFlood':'true',
            'dataType':'jsonp',
            'data':dataa
        }
        await self.my_request(method='GET',url=url,headers=self.headers,params=datas)
        my_time = int(time.time()*1000)
        sign = await self.getSign('{}&{}&12574478&'.format(self.AsyncSession.cookies.get('_m_h5_tk').split('_')[0],my_time)+dataa)
        datas['t'] = my_time
        datas['sign'] = sign
        resp = await self.my_request(method='GET',url=url,headers=self.headers,params=datas)
        return resp.json()['data']['recommend']['resultList']

    async def addDb(self,result):
        sname = ''.join(''.join(etree.HTML(result.get('itemName', '')).xpath('//text()')).split())
        c = self.session.query(commodities).filter_by(title=sname).first()
        if c==None:
            com = commodities(title=sname,
                              current_price=eval(result.get('price')),
                              promotion_price=eval(result.get('priceAfterCoupon')),
                              img_url='http:' + result.get('pic'),
                              source_url='http:' + result.get('url'),
                              site_source='淘宝网',
                              shop_name=result.get('nick'),
                              date=datetime.datetime.now())
            # print(com.title)
            self.session.add(com)
            self.session.commit()
        else:
            c:commodities
            c.title = sname,
            c.current_price = eval(result.get('price')),
            c.promotion_price = eval(result.get('priceAfterCoupon')),
            c.img_url = 'http:' + result.get('pic'),
            c.source_url = 'http:' + result.get('url'),
            c.site_source = '淘宝网',
            c.shop_name = result.get('nick'),
            c.date = datetime.datetime.now()
            self.session.commit()
    async def run(self):
        try:
            try:
                resultList = await self.getTaoBaoInfos(0,200)
            except:
                resultList = await self.getTaoBaoInfos(0,200)
            for result in resultList:
                await self.addDb(result)
        except:
            print('没有搜到该商品哟')
        self.session.close()
        await self.AsyncSession.aclose()

if __name__ == '__main__':
    t = spiderTaoBao('显卡')
    asyncio.run(t.run())