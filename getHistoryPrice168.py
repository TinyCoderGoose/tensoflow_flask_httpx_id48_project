import asyncio
import re
import time
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
        self.headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.54',
         'Content-Type':'application/x-www-form-urlencoded',
         "Cookie":'WDCH=276; PHPSESSID=ltbf3dcte9d7kgcqo50dc1jr63'
         }
        self.postdata={
        'checkCode': '7034576ad3a4e807cf513f6da8c94d8f',
        'con': id,
        }
        self.AsyncSession.headers.update(self.headers)

    async def my_request(self, method='GET', url=None, headers=None, params=None,json=None, files=None,data=None, allow_redirects=True,timeout=10):
        for _ in range(5):
            try:
                resp = await self.AsyncSession.request(method=method, url=url, headers=headers, params=params,
                                                   data=data, allow_redirects=allow_redirects, json=json, files=files,
                                                   timeout=timeout)
                return resp
            except Exception as e:
                print("错误:"+str(e))

    async def getinfo(self):
        while True:
                code = await self.get_code()
                if not code:
                    continue
                url = 'http://www.tool168.cn/dm/history.php'
                data = {
                    'code': code,
                    't': ''
                }
                while True:
                    resp = await self.my_request(method="GET",url=url,params=data,headers=self.headers)
                    try:
                        history = re.findall("chart\(\'(.*?\])\'", resp.text)[0]
                        print(history)
                        break
                    except:
                        time.sleep(1)
                        print(resp.text)
                c=self.session.query(CommodityInfo).filter_by(source_url=self.source_url).first()
                c.history_price=history
                print(c.id)
                self.session.commit()
                break
                return None


    async def get_code(self):
        url = 'http://www.tool168.cn/dm/ptinfo.php'
        resp = await self.my_request(method="POST",url=url, data=self.postdata, headers=self.headers)
        try:
            code = resp.json()['code']
        except:
            # print(resp.text)
            return None
        return code


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

