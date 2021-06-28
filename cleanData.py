import asyncio
import re

from sqlalchemy.orm import sessionmaker
import SQLModule
import pandas as pd


# [0:'七彩虹',1:'华硕']
# [0:'京东',1:'苏宁']

# [[库存,折扣,来源,品牌,型号,芯片,显存类型,显存容量,风扇,日期#时间戳年月日,是否节假],[库存,折扣,来源,品牌,型号,芯片,显存类型,显存容量,风扇,日期#时间戳年月日,是否节假]]
# [价格,价格]

async def cleanDataBase(Session_class):
    session = Session_class()
    data = session.query(SQLModule.CommodityInfo).filter_by(history_price=None).delete()
    data = session.query(SQLModule.CommodityInfo).filter_by(graphics_type='其他').delete()
    data = session.query(SQLModule.CommodityInfo).filter_by(graphics_memory='其他').delete()
    data = session.query(SQLModule.CommodityInfo).filter_by(fan_count='其他').delete()
    data = session.query(SQLModule.CommodityInfo).filter_by(model='其他').delete()
    session.commit()
    session.close()


async def brand_class(Session_class, engine):
    brand = pd.read_sql_query('SELECT brand_name From commodityInfo', engine)
    for i, r in brand.iterrows():
        if 'NVIDIA' in r['brand_name'].upper() :
            r['brand_name']='英伟达'
        if 'AMD' in r['brand_name'].upper() :
            r['brand_name'] = 'AMD'
        if 'AORUS' in r['brand_name'].upper():
            r['brand_name'] = '技嘉'
        r['brand_name'] = r['brand_name'].split("（")[0]
        r['brand_name'] = r['brand_name'].split("(")[0]
    brand=brand.drop_duplicates('brand_name',keep='first')
    brand=brand[~(brand['brand_name'].isnull())].reset_index()[['brand_name']]
    session = Session_class()
    for i in brand['brand_name']:
        x = session.query(SQLModule.tb_brand).filter_by(value=i).first()
        if x:
            continue
        else:
            tb = SQLModule.tb_brand(value=i)
            session.add(tb)
            session.commit()

async def chip_class(Session_class,engine):
    brand = pd.read_sql_query('SELECT chip_brand From commodityInfo', engine)
    brand = brand.drop_duplicates('chip_brand', keep='first')
    brand = brand[~(brand['chip_brand'].isnull())].reset_index()[['chip_brand']]
    session = Session_class()
    for i in brand['chip_brand']:
        x = session.query(SQLModule.tb_chip).filter_by(value=i).first()
        if x:
            continue
        else:
            tb = SQLModule.tb_chip(value=i)
            session.add(tb)
            session.commit()

async def fan_class(Session_class,engine):
    fan = pd.read_sql_query('SELECT fan_count From commodityInfo', engine)
    fan = fan.drop_duplicates('fan_count', keep='first')
    fan = fan[~(fan['fan_count'].isnull())].reset_index()[['fan_count']]
    session = Session_class()
    for i in fan['fan_count']:
        x = session.query(SQLModule.tb_fan).filter_by(value=i).first()
        if x:
            continue
        else:
            tb = SQLModule.tb_fan(value=i)
            session.add(tb)
            session.commit()

async def type_class(Session_class,engine):
    typec = pd.read_sql_query('SELECT graphics_type From commodityInfo', engine)
    typec = typec.drop_duplicates('graphics_type', keep='first')
    typec = typec[~(typec['graphics_type'].isnull())].reset_index()[['graphics_type']]
    session = Session_class()
    for i in typec['graphics_type']:
        x = session.query(SQLModule.tb_graphics_type).filter_by(value=i).first()
        if x:
            continue
        else:
            tb = SQLModule.tb_graphics_type(value=i)
            session.add(tb)
            session.commit()

async def memory_class(Session_class,engine):
    memory = pd.read_sql_query('SELECT graphics_memory From commodityInfo', engine)
    memory = memory.drop_duplicates('graphics_memory', keep='first')
    memory = memory[~(memory['graphics_memory'].isnull())].reset_index()[['graphics_memory']]
    session=Session_class()
    for i in memory['graphics_memory']:
        x=session.query(SQLModule.tb_graphics_memory).filter_by(value=i).first()
        if x:continue
        else:
            tb=SQLModule.tb_graphics_memory(value=i)
            session.add(tb)
            session.commit()

async def site_class(Session_class,engine):
    site_source = pd.read_sql_query('SELECT site_source From commodityInfo', engine)
    site_source = site_source.drop_duplicates('site_source', keep='first')
    site_source = site_source[~(site_source['site_source'].isnull())].reset_index()[['site_source']]
    session=Session_class()
    for i in site_source['site_source']:
        x=session.query(SQLModule.tb_graphics_memory).filter_by(value=i).first()
        if x:continue
        else:
            tb=SQLModule.tb_site(value=i)
            session.add(tb)
            session.commit()

async def model_class(Session_class,engine):
    model = pd.read_sql_query('SELECT model From commodityInfo', engine)
    model = model.drop_duplicates('model', keep='first')
    model = model[~(model['model'].isnull())].reset_index()[['model']]
    session=Session_class()
    for i in model['model']:
        x=session.query(SQLModule.tb_model).filter_by(value=i).first()
        if x:continue
        else:
            tb=SQLModule.tb_model(value=i)
            session.add(tb)
            session.commit()


async def run():
    Session_class = sessionmaker(bind=SQLModule.engine)
    await cleanDataBase(Session_class)
    await brand_class(Session_class, SQLModule.engine)
    await chip_class(Session_class, SQLModule.engine)
    await fan_class(Session_class, SQLModule.engine)
    await type_class(Session_class, SQLModule.engine)
    await memory_class(Session_class, SQLModule.engine)
    await site_class(Session_class, SQLModule.engine)
    await model_class(Session_class, SQLModule.engine)
    print("done.")

async def cleanBrand(df):
    for i,r in df.iterrows():
        r['brand_name']=''.join(re.findall("[\u4E00-\u9FA5]*",r['brand_name']))
    return df


def start():
    asyncio.run(run())


if __name__ == '__main__':
    start()
