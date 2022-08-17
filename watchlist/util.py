import warnings
warnings.filterwarnings('ignore')
import requests
import json
import demjson


class Util:
    def stock_data(code):

        urlp1='https://ig507.com/data/time/real/'
        urlp2='?licence=' #config real key
        url=urlp1 + code +urlp2
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

        resultData= str(percent) +'% - ' + str(price) +' - 开'+ str(open_price) +' - 高'+  str(high_price) +' - 低'+ str(low_price) + ' - 换' + str(hs)  +'% - 振'+ str(zf)  +'% - 交' +str(cjestr)+' - 流' + str(ltstr)

        return resultData;