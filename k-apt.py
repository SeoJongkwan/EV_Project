import pandas as pd
import numpy as np
import requests
import json
import xml.etree.ElementTree as ET
import xmltodict
import psycopg2
from datetime import datetime, timedelta
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
from urllib.parse import urlencode, unquote
import matplotlib.pyplot as plt


url = "http://apis.data.go.kr/1611000/ApHusEnergyUseInfoOfferService/getHsmpApHusUsgQtyInfoSearch"
cert_key = "oEXb0KBtqI8V3TJAj1lmb9ZgDq8pwKDDnk2dAlaRpRltMNYuoTCT%2B1hlmImqXNWjK2qquaN9S7v2irGCoRccxw%3D%3D"

date = list(range(202109, int(datetime.now().strftime("%Y%m")),1))
aptcode = ["A10025420", "A10025263", "A43576808"]
month_usage = []

def get_apt(aptcode):
    for month in date:
        params = "?" + urlencode({
            "serviceKey": cert_key,
            "kaptCode": aptcode,
            "reqDate": str(month)
        })

        res = requests.get(url+unquote(params))
        content = res.content
        data = xmltodict.parse(content)
        dict = json.loads(json.dumps(data))
        month_usage.append(dict)

        # df = pd.DataFrame(dict['response']['body']).reset_index()
        # df['month'] = month
        # df1 = df.pivot(index='index', columns='month', values='item')
    return month_usage


apt1 = get_apt(aptcode[0])
apt2 = get_apt(aptcode[1])
apt3 = get_apt(aptcode[2])


df1 = pd.DataFrame(apt1[0]['response']['body']).reset_index()
df1['month'] = date[0]
df1 = df1.pivot(index='index', columns='month', values='item')
df2 = pd.DataFrame(apt1[1]['response']['body']).reset_index()
df2['month'] = date[1]
df2 = df2.pivot(index='index', columns='month', values='item')
df3 = pd.DataFrame(apt1[2]['response']['body']).reset_index()
df3['month'] = date[2]
df3 = df3.pivot(index='index', columns='month', values='item')

df = pd.concat([df1, df2], axis=1)
df = pd.concat([df, df3], axis=1)
dft = df.T.sort_index(ascending=False)
dft = dft[['helect']]


cf1 = pd.DataFrame(apt1[3]['response']['body']).reset_index()
cf1['month'] = date[0]
cf1 = cf1.pivot(index='index', columns='month', values='item')
cf2 = pd.DataFrame(apt1[4]['response']['body']).reset_index()
cf2['month'] = date[1]
cf2 = cf2.pivot(index='index', columns='month', values='item')
cf3 = pd.DataFrame(apt1[5]['response']['body']).reset_index()
cf3['month'] = date[2]
cf3 = cf3.pivot(index='index', columns='month', values='item')

cf = pd.concat([cf1, cf2], axis=1)
cf = pd.concat([cf, cf3], axis=1)
cft = cf.T.sort_index(ascending=False)
cft = cft[['helect']]


bf1 = pd.DataFrame(apt1[6]['response']['body']).reset_index()
bf1['month'] = date[0]
bf1 = bf1.pivot(index='index', columns='month', values='item')
bf2 = pd.DataFrame(apt1[7]['response']['body']).reset_index()
bf2['month'] = date[1]
bf2 = bf2.pivot(index='index', columns='month', values='item')
bf3 = pd.DataFrame(apt1[8]['response']['body']).reset_index()
bf3['month'] = date[2]
bf3 = bf3.pivot(index='index', columns='month', values='item')

bf = pd.concat([bf1, bf2], axis=1)
bf = pd.concat([bf, bf3], axis=1)
bft = bf.T.sort_index(ascending=False)
bft = bft[['helect']]

af = pd.concat([dft, cft], axis=1)
af = pd.concat([af, bft], axis=1)
af.columns = aptcode

# def show_month_electric(df):
#     plt.rc('font', family='AppleGothic', size=10)
#     plt.bar(['202109', '202110', '202111'], df['helect'])
#     plt.title("아파트 공용부 전력현황")
#     plt.ylabel('kWh')
#     plt.grid(True, axis='y', linestyle='dashed', alpha=0.4)
#     plt.legend(loc=1)
#     plt.tight_layout()
#     plt.show()
#
# show_month_electric(dft)
