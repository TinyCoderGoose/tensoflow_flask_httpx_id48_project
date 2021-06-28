from sqlalchemy import *
from sqlalchemy.orm import declarative_base, sessionmaker
import settings

DIALECT = settings.DIALECT
DRIVER = settings.DRIVER
USERNAME = settings.USERNAME
PASSWORD = settings.PASSWORD
HOST = settings.HOST
PORT = settings.PORT
DATABASE = settings.DATABASE
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                       PORT, DATABASE)
engine = create_engine(SQLALCHEMY_DATABASE_URI)
Base = declarative_base()


class CommodityInfo(Base):
    __tablename__ = "commodityInfo"
    id = Column(INTEGER, primary_key=True)
    title = Column(String)
    source_url = Column(String)
    img_url = Column(String)
    current_price = Column(DECIMAL)
    stock = Column(String)
    discount = Column(String)
    site_source = Column(String)
    brand_name = Column(String)
    model = Column(String)
    chip_brand = Column(String)
    graphics_type = Column(String)
    graphics_memory = Column(String)
    fan_count = Column(String)
    shop_name = Column(String)
    history_price = Column(TEXT)
    date = Column(DATETIME)
    is_holiday = Column(INTEGER)

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


class commodities(Base):
    __tablename__ = "commodities"
    id = Column(INTEGER, primary_key=True)
    title = Column(String)
    current_price = Column(DECIMAL)
    promotion_price = Column(DECIMAL)
    img_url = Column(String)
    source_url = Column(String)
    site_source = Column(String)
    shop_name = Column(String)
    date = Column(DATETIME)

    def get_dict(self):
        return {'id': self.id,
                'title': self.title,
                "current_price": self.current_price,
                "promotion_price": self.promotion_price,
                "img_url": self.img_url,
                'source_url': self.source_url,
                "site_source": self.site_source,
                "shop_name": self.shop_name,
                "date": self.date,
                }

class tb_brand(Base):
    __tablename__="tb_brand"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_chip(Base):
    __tablename__="tb_chip"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_fan(Base):
    __tablename__="tb_fan"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_graphics_memory(Base):
    __tablename__="tb_graphics_memory"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_graphics_type(Base):
    __tablename__="tb_graphics_type"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_model(Base):
    __tablename__="tb_model"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)

class tb_site(Base):
    __tablename__="tb_site"
    id=Column(INTEGER,primary_key=True)
    value=Column(String)