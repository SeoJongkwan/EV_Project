import pandas as pd
import argparse
import os
import re
from common import Data         #common class
import chart

pd.set_option('mode.chained_assignment', None) # SettingWithCopyWarning

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()

PATH = '/Users/bellk/ION/2021.양방향 정보 기반 공동주택 스마트 충전시스템 서비스 개발 및 실증/2.연구/기관/1.클린일렉스/'
path1 = PATH + '급속충전기 로그데이터 2109/'
path2 = PATH + '급속충전기 로그데이터 2110/'
path3 = PATH + '급속충전기 로그데이터 2111/'

charger = file.file_name[0]

file1 = '인덕원IT밸리 충전기이용내역 2109.csv'
file2 = '인덕원IT밸리 충전기이용내역 2110.csv'
file3 = '인덕원IT밸리 충전기이용내역 2111.csv'

user9 = pd.read_csv(path1 + file1, encoding='UTF8')
user10 = pd.read_csv(path2 + file2, encoding='UTF8')
user11 = pd.read_csv(path3 + file3, encoding='UTF8')

merge_data = []
merge_data.append(user9)
merge_data.append(user10)
merge_data.append(user11)

df1 = pd.concat(merge_data)

col = '이용자이름'
df1[col].unique()
df1[col].value_counts()
df1[col].value_counts().sum()

len(df1[col].unique())

chart.show_value_cnt(df1, charger, '이용자이름', 'green')



# print("\ncolumn name change: kor --> eng")
# user_col = ['SID', 'time', 'charger', 'AS', 'chargerNo', 'user', 'carNo', 'duration', 'AccumulatedWatt',
#             'chargingFee', 'payment', 'payMethod', 'roaming', 'roamingNo', 'status', 'chargerStatus']
# df1.columns = user_col

# print("user column char remove")
# user_file['user'] = [re.sub('[()가-힣]', '', s) for s in user_file['user']]
#
# print('time column split --> start & end')
# user_file.insert(1, 'start', user_file['time'].str.split('~').str[0])
# user_file.insert(2, 'end', user_file['time'].str.split('~').str[1])
# user_file['start'] = user_file['start'].str.rstrip()
# user_file['start'] = pd.to_datetime(user_file['start'], format='%y/%m/%d %H:%M')
# user_file['end'] = user_file['end'].str.lstrip()
# user_file['end'] = pd.to_datetime(user_file['end'], format='%y/%m/%d %H:%M')
#
# # user_file['start'] = user_file['start'].dt.strftime('%Y-%m-%d %H:%M')
# # user_file['end'] = user_file['end'].dt.strftime('%Y-%m-%d %H:%M')
#
# print('duration(h:m:s) column transform --> second')
# user_file['second'] = 0
# user_file['minute'] = 0
# user_file['hour'] = 0
#
# user_file['duration'].str.strip()
# for i in range(len(user_file)):
#     locate = user_file['duration'][i].find('초')
#     if locate != -1:
#         user_file['second'][i] = int(user_file['duration'][i][locate - 3:locate])
#     else:
#         pass
#
# for i in range(len(user_file)):
#     locate = user_file['duration'][i].find('분')
#     if locate != -1:
#         if locate > 2:
#             user_file['minute'][i] = int(user_file['duration'][i][locate - 3:locate]) * 60
#         else:
#             user_file['minute'][i] = int(user_file['duration'][i][:locate].rstrip()) * 60
#     else:
#         pass
#
# for i in range(len(user_file)):
#     locate = user_file['duration'][i].find('시간')
#     if locate != -1:
#         if locate > 2:
#             user_file['hour'][i] = int(user_file['duration'][i][locate - 3:locate]) * 3600
#         else:
#             user_file['hour'][i] = int(user_file['duration'][i][:locate].rstrip()) * 3600
#     else:
#         pass
#
# for i in range(len(user_file)):
#     user_file['duration'][i] = user_file['hour'][i]+user_file['minute'][i]+user_file['second'][i]
#
# drop_col = ['time','hour','minute','second']
# user_file = user_file.drop(drop_col, axis=1)
# print("drop columns", drop_col)
# user_file = user_file.sort_values(by='start',ascending=True).reset_index(drop=True)
#
# transform_file = 'dc_100kW_user.csv'
# print("\ntransform file:", transform_file)
# user_file.to_csv(args.data_path + transform_file, index=False)

