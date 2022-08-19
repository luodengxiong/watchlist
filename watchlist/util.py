import datetime
import warnings
warnings.filterwarnings('ignore')
import requests
import json
import demjson

from watchlist import app, db
from watchlist.models import Config
from watchlist.zhangtingmodel import Zhangting


licenseconfig = Config.query.filter(Config.name == 'license').first()

license='licence='+licenseconfig.value; #config real key

class Util:
    def stock_data(code):

        urlp1='https://ig507.com/data/time/real/'
        url=urlp1 + code +'?'+license
        #print(url)
        jsondata = requests.get(url).json()

        percent=jsondata['pc']
        hs=jsondata['hs']
        price=jsondata['p']
        open_price=jsondata['o']
        high_price=jsondata['h']
        low_price=jsondata['l']
        zf=jsondata['zf']
        cje=jsondata['cje'] #成交额（元）
        lt=jsondata['lt'] #流通市值（元）
        cjeInt = int(cje)


        cjestr = '%.2f' % (cjeInt / 100000000) + '亿';
        ltInt = int(lt)
        ltstr = '%.2f' % (ltInt / 100000000) + '亿';

        resultData='[' + str(percent) +'%] - ' + str(price) +' - 开'+ str(open_price) +' - 高'+  str(high_price) +' - 低'+ str(low_price) + ' - 换' + str(hs)  +'% - 振'+ str(zf)  +'% - 交' +str(cjestr)+' - 流' + str(ltstr)

        return resultData;

    #定义初始化涨停数据的方法，参数为日期（格式yyyy-MM-dd）
    #API：https://ig507.com/data/time/zdtgc/ztgc/ 日期 ?licence= 您的licence
    #描述：根据日期（格式yyyy-MM-dd，从2019-11-28开始到现在的每个交易日）作为参数，得到每天的涨停股票列表，根据封板时间升序。
    #考虑部署到线上，定时执行，一般设置为收盘后执行，目的是用于次日上午集合竞价观察分析
    def zhangting_data(date_str):
        #db.create_all()
        urlp1 = 'https://ig507.com/data/time/zdtgc/ztgc/'
        url = urlp1 + date_str + '?' + license
        jsondata = requests.get(url).json()
        for m in jsondata:
            # dm = db.Column(db.String(10))  # 代码
            # mc = db.Column(db.String(10))  # 名称
            # p = db.Column(db.Float)  # 价格（元）
            # zf = db.Column(db.Float)  # 涨幅（%）
            # hs = db.Column(db.Float)  # 换手率（%）
            # lbc = db.Column(db.Integer)  # 连板数
            # zbc = db.Column(db.Integer)  # 炸板数
            # zj = db.Column(db.BigInteger)  # 封板资金（元）
            # cje = db.Column(db.BigInteger)  # 成交额（元）
            # lt = db.Column(db.BigInteger)  # 流通市值（元）
            # zsz = db.Column(db.BigInteger)  # 总市值（元）
            # tj = db.Column(db.String(10))  # 涨停统计（x天/y板）
            # fbt = db.Column(db.String(10))  # 首次封板时间（HH:mm:ss）
            # lbt = db.Column(db.String(10))  # 最后封板时间（HH:mm:ss）
            # riqi = db.Column(db.Date)  # 数据所属日期
            zhangting = Zhangting(dm=m['dm'],
                                  mc=m['mc'],
                                  p=m['p'],
                                  zf=m['zf'],
                                  hs=m['hs'],
                                  lbc=m['lbc'],
                                  zbc=m['zbc'],
                                  zj=m['zj'],
                                  cje=m['cje'],
                                  lt=m['lt'],
                                  zsz=m['zsz'],
                                  tj=m['tj'],
                                  fbt=m['fbt'],
                                  lbt=m['lbt'],
                                  riqi= datetime.datetime.strptime(date_str,'%Y-%m-%d'),
                                  timestamp=datetime.datetime.now()
                                  )
            db.session.add(zhangting)


        db.session.commit()

        return 'Data commit.';

    ###把查询到的数据库对象转换为json，方便调试
    def to_dict(self):
        result = {}
        for key in self.__mapper__.c.keys():
            if getattr(self, key) is not None:
                result[key] = str(getattr(self, key))
            else:
                result[key] = getattr(self, key)
        return result