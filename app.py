import asyncio
import datetime
import json
import os
import random
import time
import numpy as np
from flask import Flask, make_response, render_template, session, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from matplotlib.font_manager import _JSONEncoder
from sqlalchemy import func, or_
import Date
from forecast import *
from settings import *
from test import spiderRun
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
app.config['SQLALCHEMY_ECHO'] = SQLALCHEMY_ECHO
app.config['SECRET_KEY'] = os.urandom(30)


class CommodityInfo(db.Model):
    __tablename__ = "commodityInfo"
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String)
    source_url = db.Column(db.String)
    img_url = db.Column(db.String)
    current_price = db.Column(db.DECIMAL)
    stock = db.Column(db.String)
    discount = db.Column(db.String)
    site_source = db.Column(db.String)
    brand_name = db.Column(db.String)
    model = db.Column(db.String)
    chip_brand = db.Column(db.String)
    graphics_type = db.Column(db.String)
    graphics_memory = db.Column(db.String)
    fan_count = db.Column(db.String)
    shop_name = db.Column(db.String)
    history_price = db.Column(db.TEXT)
    date = db.Column(db.DATETIME)
    is_holiday = db.Column(db.INTEGER)

    def get_dict(self):
        return {'id': self.id, 'title': self.title, 'source_url': self.source_url, "img_url": self.img_url,
                "current_price": self.current_price,
                "stock": self.stock,
                "discount": self.discount,
                "site_source": self.site_source,
                "brand_name": self.brand_name,
                "model": self.model,
                "chip_brand": self.chip_brand,
                "graphics_type": self.graphics_type,
                "graphics_memory": self.graphics_memory,
                "fan_count": self.fan_count,
                "shop_name": self.shop_name,
                "history_price": self.history_price,
                "date": self.date,
                "is_holiday": self.is_holiday}


class tb_Brand(db.Model):
    __tablename__ = "tb_brand"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}


class tb_Chip(db.Model):
    __tablename__ = "tb_chip"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}


class tb_Model(db.Model):
    __tablename__ = "tb_model"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}


class tb_Graphics_memory(db.Model):
    __tablename__ = "tb_graphics_memory"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}

class tb_Site(db.Model):
    __tablename__ = "tb_site"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}


class tb_Fan(db.Model):
    __tablename__ = "tb_fan"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)

    def get_dict(self):
        return {'id': self.id, 'value': self.value}


class forecast_Price(db.Model):
    __tablename__ = "forecast_price"
    id = db.Column(db.INTEGER, primary_key=True)
    model_id = db.Column(db.INTEGER)
    m_time = db.Column(db.DATETIME)
    price = db.Column(db.DECIMAL)

    def get_dict(self):
        return {'id': self.id, 'model_id': self.model_id, 'm_time': self.m_time, 'price': self.price}


class tb_Graphics_type(db.Model):
    __tablename__ = "tb_graphics_type"
    id = db.Column(db.INTEGER, primary_key=True)
    value = db.Column(db.String)
    def get_dict(self):
        return {'id': self.id, 'value': self.value}

class Commodities(db.Model):
    __tablename__ = "commodities"
    id = db.Column(db.INTEGER, primary_key=True)
    title = db.Column(db.String)
    current_price = db.Column(db.DECIMAL)
    promotion_price = db.Column(db.DECIMAL)
    img_url = db.Column(db.String)
    source_url = db.Column(db.String)
    site_source = db.Column(db.String)
    shop_name = db.Column(db.String)
    date = db.Column(db.DATETIME)

    def get_dict(self):
        return {'id': self.id,
                'title': self.title,
                "current_price": float(self.current_price),
                "promotion_price": float(self.promotion_price),
                "img_url": self.img_url,
                'source_url': self.source_url,
                "site_source": self.site_source,
                "shop_name": self.shop_name,
                "date": self.date.strftime('%Y-%m-%d %H:%M:%S')}

class Tb_hot_keyword(db.Model):
    __tablename__ = "tb_hot_keyword"
    id = db.Column(db.INTEGER, primary_key=True)
    keyword = db.Column(db.String)
    times = db.Column(db.INTEGER)

    def get_dict(self):
        return {'id': self.id, 'keyword': self.keyword, 'times': self.times}

@app.route('/')
def index():
    keywords = []
    a = Tb_hot_keyword.query.order_by(Tb_hot_keyword.times.desc()).all()
    for i in range(len(a)):
        if i > 4: break
        keywords.append(a[i].keyword)
    return render_template('search.html', keywords=keywords,title = '没啥用●没心思想●的●搜索引擎')

@app.route('/max')
def max():
    return render_template('index.html', title='多电商显卡价格可视化平台')




@app.route('/api/create_data')
def create_data():
    res = CommodityInfo().query.all()
    tb_brands = []
    tb_chips = []
    tb_fans = []
    tb_graphics_memorys = []
    tb_graphics_types = []
    tb_models = []
    tb_sites = []
    for r in res:
        r: CommodityInfo
        if not r.brand_name in tb_brands:
            tb_brands.append(r.brand_name)
        if not r.chip_brand in tb_chips:
            tb_chips.append(r.chip_brand)
        if not r.fan_count in tb_fans:
            tb_fans.append(r.fan_count)
        if not r.graphics_memory in tb_graphics_memorys:
            tb_graphics_memorys.append(r.graphics_memory)
        if not r.graphics_type in tb_graphics_types:
            tb_graphics_types.append(r.graphics_type)
        if not r.model in tb_models:
            tb_models.append(r.model)
        if not r.site_source in tb_sites:
            tb_sites.append(r.site_source)
    for t in tb_brands:
        if tb_Brand.query.filter_by(value=t).first(): continue
        tb = tb_Brand()
        tb.value = t
        db.session.add(tb)
    for t in tb_chips:
        if tb_Chip.query.filter_by(value=t).first(): continue
        tb = tb_Chip()
        tb.value = t
        db.session.add(tb)
    for t in tb_fans:
        if tb_Fan.query.filter_by(value=t).first(): continue
        tb = tb_Fan()
        tb.value = t
        db.session.add(tb)
    for t in tb_graphics_memorys:
        if tb_Graphics_memory.query.filter_by(value=t).first(): continue
        tb = tb_Graphics_memory()
        tb.value = t
        db.session.add(tb)
    for t in tb_graphics_types:
        if tb_Graphics_type.query.filter_by(value=t).first(): continue
        tb = tb_Graphics_type()
        tb.value = t
        db.session.add(tb)
    for t in tb_models:
        if tb_Model.query.filter_by(value=t).first(): continue
        tb = tb_Model()
        tb.value = t
        db.session.add(tb)
    for t in tb_sites:
        if tb_Site.query.filter_by(value=t).first(): continue
        tb = tb_Site()
        tb.value = t
        db.session.add(tb)
    db.session.commit()
    return 'ok'


def get_sql_infos():
    res = CommodityInfo().query.all()
    sites = tb_Site.query.all()
    models = tb_Model.query.all()
    graphics_types = tb_Graphics_type.query.all()
    graphics_memorys = tb_Graphics_memory.query.all()
    fans = tb_Fan.query.all()
    chips = tb_Chip.query.all()
    brands = tb_Brand.query.all()
    train_data = []
    train_labels = []
    for r in res:
        r: CommodityInfo
        try:
            history_price = eval('[' + r.history_price + ']')
            for h in history_price:
                mtime = h[0]
                mprice = h[1]
                msite = 0
                for s in sites:
                    s: tb_Site
                    if r.site_source in s.value or s.value in r.site_source:
                        msite = s.id
                        break
                mmodel = 0
                for m in models:
                    m: tb_Model
                    if r.model in m.value or m.value in r.model:
                        mmodel = m.id
                        break
                mgraphics_type = 0
                for g in graphics_types:
                    g: tb_Graphics_type
                    if r.graphics_type in g.value or g.value in r.graphics_type:
                        mgraphics_type = g.id
                        break
                mgraphics_memory = 0
                for g in graphics_memorys:
                    g: tb_Graphics_memory
                    if r.graphics_memory in g.value or g.value in r.graphics_memory:
                        mgraphics_memory = g.id
                        break
                mfan = 0
                for f in fans:
                    f: tb_Fan
                    if r.fan_count in f.value or f.value in r.fan_count:
                        mfan = f.id
                        break
                mchip = 0
                for c in chips:
                    c: tb_Chip
                    if r.chip_brand in c.value or c.value in r.chip_brand:
                        mchip = c.id
                        break
                mbrand = 0
                for b in brands:
                    b: tb_Brand
                    if b.value in r.brand_name or r.brand_name in b.value:
                        mbrand = b.id
                        break
                train_data.append(
                    [float(mtime), float(msite), float(mmodel), float(mgraphics_type), float(mgraphics_memory),
                     float(mfan), float(mchip), float(mbrand)])
                train_labels.append(mprice)
        except:
            continue
    return train_data,train_labels

@app.route('/api/t_v1/get_train_datas')
def get_train_datas():
    try:
        train_data, train_labels = get_sql_infos()
        return {'code':0,'train_data':train_data,'train_labels':train_labels,'quantity':len(train_labels)}
    except:
        return {'code':0,'msg':'api error'}

@app.route('/api/t_v1/get_tens_model_infos',methods=['POST', 'GET'])
def get_tens_model_infos():
    train_data, train_labels = get_sql_infos()
    resodata = {'train': train_data, 'train_labels': train_labels}
    train_data = np.array(train_data)
    train_labels = np.array(train_labels)
    test_data = train_data
    test_labels = train_labels
    (train_data, train_labels), (test_data, test_labels) = pretreatment(train_data, train_labels, test_data,
                                                                        test_labels)
    model = build_model(train_data)
    model.load_weights('./forecast.h5')
    # model = my_fit(model, train_data, train_labels, len(resodata['train_labels']))
    # model.save('./forecast.h5')
    test_predictions = model.predict(test_data).flatten()
    dates = []
    for d in resodata['train'][-12:]:
        timeStamp = int(d[0])
        dateArray = datetime.datetime.fromtimestamp(timeStamp)
        dates.append(dateArray.strftime('%Y-%m-%d'))
    plotVersusFigure(test_labels, test_predictions)
    # print(type(resodata['train_labels'][-12:][0]))
    resp_info = {'times':dates,'real_price':[round(float(a),2) for a in resodata['train_labels'][-12:]],'predict_price':[round(float(i),2) for i in test_predictions[-12:]]}
    return resp_info

def plotVersusFigure(y_true_price, y_predict_price):
    plt.figure(figsize=(10, 7))
    x_show = np.rint(np.linspace(1, np.max(y_true_price), len(y_true_price))).astype(int)
    plt.plot(x_show, y_true_price, 'o-', color='w')
    x_show_predicted = np.rint(np.linspace(1, np.max(y_predict_price), len(y_predict_price))).astype(int)
    plt.plot(x_show_predicted, y_predict_price, 'o-', color='m')
    plt.title('MODEL FORECAST', color='w')
    plt.legend(loc='lower right', labels=["True Prices", "Predicted Prices"])
    plt.xlabel("x",color='w')
    plt.ylabel("y",color='w')
    plt.tick_params(axis='x',colors='w')
    plt.tick_params(axis='y',colors='w')
    plt.savefig("static/images/forecast.png",transparent = True)
    # plt.show()

@app.route('/api/t_v1/get_model_avg')
def get_model_avg():
    modelname = request.args.get('modelname')
    resp = {'code': 0, 'avg_price': 0}
    if modelname:
        minaa = db.session.query(func.avg(CommodityInfo.current_price).label('average')).filter(
            CommodityInfo.model.like('%{}%'.format(modelname))).first()
        resp['avg_price'] = str(round(float(minaa[0]),2))
    else:
        minaa = db.session.query(func.avg(CommodityInfo.current_price).label('average')).filter(
            CommodityInfo.model.like('%3070%')).first()
        resp['avg_price'] = str(round(float(minaa[0]),2))
    return resp

@app.route('/api/t_v1/get_model_max')
def get_model_max():
    modelname = request.args.get('modelname')
    resp = {'code': 0, 'datas': []}
    if modelname:
        minaa = db.session.query(CommodityInfo).filter(CommodityInfo.model.like('%{}%'.format(modelname))).order_by(
            CommodityInfo.current_price.desc()).all()
        for d in minaa:
            if len(resp['datas']) > 4: break
            resp['datas'].append([d.site_source, d.model, str(d.current_price)])
    else:
        minaa = db.session.query(CommodityInfo).filter(CommodityInfo.model.like('%3070%')).order_by(CommodityInfo.current_price.desc()).all()
        for d in minaa:
            if len(resp['datas']) > 4: break
            resp['datas'].append([d.site_source,d.model,str(d.current_price)])
    return resp

@app.route('/api/t_v1/get_model_min')
def get_model_min():
    modelname = request.args.get('modelname')
    resp = {'code': 0, 'datas': []}
    if modelname:
        minaa = db.session.query(CommodityInfo).filter(CommodityInfo.model.like('%{}%'.format(modelname))).order_by(
            CommodityInfo.current_price).all()
        for d in minaa:
            if len(resp['datas']) > 4: break
            resp['datas'].append([d.site_source, d.model, str(d.current_price)])
    else:
        minaa = db.session.query(CommodityInfo).filter(CommodityInfo.model.like('%3070%')).order_by(
            CommodityInfo.current_price).all()
        for d in minaa:
            if len(resp['datas'])>4:break
            resp['datas'].append([d.site_source, d.model, str(d.current_price)])
    return resp

@app.route('/api/t_v1/get_wrap_ls', methods=['POST', 'GET'])
def get_wrap_ls():
    try:
        res = CommodityInfo().query.all()
        resp = {'code': 0, 'data': [], 'models': []}
        for r in res:
            if len(''.join(r.model.split())) > 11: continue
            if not ''.join(r.model.split()) in resp['models']:
                resp['models'].append(''.join(r.model.split()))
            resp['data'].append(
                [r.site_source, float(r.current_price), ''.join(r.model.split()), r.date.strftime('%Y-%m-%d')])
        return resp
    except Exception as e:
        print(e)
        return {'code': 2}

@app.route('/api/t_v1/get_historyPrices')
def get_histotyPrices():
    modelname = request.args.get('modelname')
    resp = {'code': 0, 'times': [], 'names': [], 'datas': []}
    jingdongdatas = {'aname': '京东', 'time': [], 'data': []}
    suningdatas = {'aname': '苏宁', 'time': [], 'data': []}
    if modelname:
        commodityinfos = CommodityInfo().query.filter(CommodityInfo.model.like('%{}%'.format(modelname))).all()
        for commodityinfo in commodityinfos:
            try:
                history_prices = eval('[' + commodityinfo.history_price + ']')
            except:
                continue
            if len(history_prices) < 13: continue
            if '京东' in commodityinfo.site_source:
                if len(jingdongdatas['time']) > 11: continue
                jingdongdatas['aname'] = commodityinfo.site_source
                for h in history_prices:
                    timeStamp = int(h[0])
                    dateArray = datetime.datetime.fromtimestamp(timeStamp)
                    jingdongdatas['time'].append(dateArray.strftime('%Y-%m-%d'))
                    jingdongdatas['data'].append(h[1])
                    if len(jingdongdatas['time']) >= 12: break
            elif '苏宁' in commodityinfo.site_source:
                if len(suningdatas['time']) > 11: continue
                suningdatas['aname'] = commodityinfo.site_source
                for h in history_prices:
                    timeStamp = int(h[0])
                    dateArray = datetime.datetime.fromtimestamp(timeStamp)
                    suningdatas['time'].append(dateArray.strftime('%Y-%m-%d'))
                    suningdatas['data'].append(h[1])
                    if len(suningdatas['time']) >= 12: break

    else:
        commodityinfos = CommodityInfo().query.filter(CommodityInfo.model.like('%3070%')).all()
        for commodityinfo in commodityinfos:
            try:
                history_prices = eval('[' + commodityinfo.history_price + ']')
            except:
                continue
            if len(history_prices) < 13: continue
            if '京东' in commodityinfo.site_source:
                if len(jingdongdatas['time']) > 11: continue
                jingdongdatas['aname'] = commodityinfo.site_source
                for h in history_prices:
                    timeStamp = int(h[0])
                    dateArray = datetime.datetime.fromtimestamp(timeStamp)
                    jingdongdatas['time'].append(dateArray.strftime('%Y-%m-%d'))
                    jingdongdatas['data'].append(h[1])
                    if len(jingdongdatas['time']) >= 12: break
            elif '苏宁' in commodityinfo.site_source:
                if len(suningdatas['time']) > 11: continue
                suningdatas['aname'] = commodityinfo.site_source
                for h in history_prices:
                    timeStamp = int(h[0])
                    dateArray = datetime.datetime.fromtimestamp(timeStamp)
                    suningdatas['time'].append(dateArray.strftime('%Y-%m-%d'))
                    suningdatas['data'].append(h[1])
                    if len(suningdatas['time']) >= 12: break
    resp['names'] = [jingdongdatas['aname'], suningdatas['aname']]
    resp['datas'] = [jingdongdatas['data'], suningdatas['data']]
    resp['times'] = [jingdongdatas['time'], suningdatas['time']]
    return resp

@app.route('/api/t_v1/test', methods=['POST', 'GET'])
def api_test():
    return {'code': 0, 'data': ['接口测试']}


@app.route('/api/t_v1/get_hotkeyword', methods=['POST', 'GET'])
def get_hotkeyword():
    resp = {'code': 0, 'data': []}
    # minaa = db.session.query(func.max(CommodityInfo.current_price).label('average')).filter(
    #     CommodityInfo.model.like('%{}%'.format(modelname))).first()
    a = Tb_hot_keyword.query.order_by(Tb_hot_keyword.times.desc()).all()
    for i in range(len(a)):
        if i > 4: break
        resp['data'].append(a[i].keyword)
    return resp


@app.route('/api/t_v1/get_api_paging', methods=['POST', 'GET'])
def get_api_paging():
    # try:
    page = eval(request.args.get('page', '1'))
    limit = request.args.get('limit', False)
    sort = request.args.get('sorted', 'default')
    sites = request.args.get('sites', '').split('_')
    sites = [i for i in sites if i]
    keyword = request.args.get('keyword', "")
    if keyword=='NONE':
        keyword=request.cookies.get('keyword','显卡')
    hk_times = Tb_hot_keyword.query.filter_by(keyword=keyword).first()
    if hk_times:
        hk_times: Tb_hot_keyword
        hk_times.times += 1
        db.session.commit()
    else:
        hk = Tb_hot_keyword()
        hk.keyword = keyword
        hk.times = 1
        db.session.add(hk)
        db.session.commit()
        spiderRun(keyword)
    res = {"code": 0, "msg": "", "count": 0, "data": []}

    if limit:
        if sort != 'default':
            if sort == 'desc':
                if len(sites) == 3:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).order_by(
                        Commodities.promotion_price.desc()).paginate(page=page,
                                                                     per_page=int(
                                                                         limit))
                elif len(sites) == 2:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                    , or_(Commodities.site_source.like('%{}%'.format(sites[0])),
                                                          Commodities.site_source.like(
                                                              '%{}%'.format(sites[1])))).order_by(
                        Commodities.promotion_price.desc()).paginate(
                        page=page,
                        per_page=int(
                            limit))
                elif len(sites) == 1:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                    , Commodities.site_source.like('%{}%'.format(sites[0]))).order_by(
                        Commodities.promotion_price.desc()).paginate(
                        page=page,
                        per_page=int(
                            limit))
                else:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).order_by(
                        Commodities.promotion_price.desc()).paginate(page=page,
                                                                     per_page=int(
                                                                         limit))
            else:
                if len(sites) == 3:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).order_by(
                        Commodities.promotion_price).paginate(page=page,
                                                              per_page=int(
                                                                  limit))
                elif len(sites) == 2:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                    , or_(Commodities.site_source.like('%{}%'.format(sites[0])),
                                                          Commodities.site_source.like(
                                                              '%{}%'.format(sites[1])))).order_by(
                        Commodities.promotion_price).paginate(
                        page=page,
                        per_page=int(
                            limit))
                elif len(sites) == 1:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                    , Commodities.site_source.like('%{}%'.format(sites[0]))).order_by(
                        Commodities.promotion_price).paginate(
                        page=page,
                        per_page=int(
                            limit))
                else:
                    allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).order_by(
                        Commodities.promotion_price).paginate(page=page,
                                                              per_page=int(
                                                                  limit))
        else:
            if len(sites) == 3:
                allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).paginate(page=page,
                                                                                                         per_page=int(
                                                                                                             limit))
            elif len(sites) == 2:
                allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                , or_(Commodities.site_source.like('%{}%'.format(sites[0])),
                                                      Commodities.site_source.like('%{}%'.format(sites[1])))).paginate(
                    page=page,
                    per_page=int(
                        limit))
            elif len(sites) == 1:
                allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))
                                                , Commodities.site_source.like('%{}%'.format(sites[0]))).paginate(
                    page=page,
                    per_page=int(
                        limit))
            else:
                allu = Commodities.query.filter(Commodities.title.like('%{}%'.format(keyword))).paginate(page=page,
                                                                                                         per_page=int(
                                                                                                             limit))
        res['count'] = allu.total
        for u in allu.items:
            res['data'].append(u.get_dict())
    else:
        allu = Commodities.query.paginate()
        res['count'] = allu.total
        for u in allu.items:
            res['data'].append(u.get_dict())
    resp=make_response()
    resp.set_cookie("keyword",keyword,max_age=300)
    return res


# except Exception as e:
#     return {'code':1,'msg':'api error'}


@app.before_request
def before():
    '''过滤器'''
    pass


if __name__ == '__main__':
    db.create_all()
    app.run(host='0.0.0.0', port=8081)
