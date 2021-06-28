DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'hxr'
PASSWORD = 'rN5KL4kyJxL8mwr8'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'hxrtest'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                       PORT, DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False  #sql日志
myxg_modelss=[[float(1625068800),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1627747200),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1630425600),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1633017600),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1635696000),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1638288000),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1640966400),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1643644800),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1646064000),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1648742400),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1651334400),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],
        [float(1654012800),float(1),float(10),float(3),float(1),float(1),float(1),float(17)],]