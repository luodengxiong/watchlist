from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from watchlist import db



class Zhangting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dm = db.Column(db.String(10)) #代码
    mc = db.Column(db.String(10)) #名称
    p = db.Column(db.Float) #价格（元）
    zf =db.Column(db.Float) #涨幅（%）
    hs =db.Column(db.Float) #换手率（%）
    lbc = db.Column(db.Integer) #连板数
    zbc = db.Column(db.Integer) #炸板数
    zj =db.Column(db.BigInteger) #封板资金（元）
    cje =db.Column(db.BigInteger) #成交额（元）
    lt =db.Column(db.BigInteger) #流通市值（元）
    zsz =db.Column(db.BigInteger) #总市值（元）
    tj = db.Column(db.String(10)) #涨停统计（x天/y板）
    fbt = db.Column(db.String(10)) #首次封板时间（HH:mm:ss）
    lbt = db.Column(db.String(10)) #最后封板时间（HH:mm:ss）
    riqi =db.Column(db.Date) #数据所属日期
    timestamp = db.Column(db.DateTime, default=datetime.now(), index=True) #创建日期

