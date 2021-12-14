import pandas as pd
from tqdm import tqdm
from common import Data                     #common class

pd.set_option('mode.chained_assignment', None)

file = Data()
print(file.file_name)

PATH = '/Users/bellk/ION/2021.양방향 정보 기반 공동주택 스마트 충전시스템 서비스 개발 및 실증/2.연구/기관/1.클린일렉스/'
path1 = PATH + '급속충전기 로그데이터 2109/'
path2 = PATH + '급속충전기 로그데이터 2110/'
path3 = PATH + '급속충전기 로그데이터 2111/'


file_name1 = file.file_name[0]
file_name2 = file.file_name[1]
file_name3 = file.file_name[2]
file_name4 = file.file_name[3]
file_name5 = file.file_name[4]

select_file = file_name1

file1 = '인덕원IT밸리(100kW) 2109.csv'
file2 = '인덕원IT밸리 급속(100kW) 2109.csv'
file3 = '인덕원IT밸리 급속(100kW) 2109.csv'

m9 = pd.read_csv(path1 + file1)
m10 = pd.read_csv(path2 + file2)
m11 = pd.read_csv(path3 + file3)

merge_data = []
merge_data.append(m9)
merge_data.append(m10)
merge_data.append(m11)

df1 = pd.concat(merge_data)
df2 = df1.sort_values('RegDt', ascending=True).reset_index(drop=True)
df3 = df2.drop_duplicates(['RegDt', 'Send', 'msg'], keep='first').reset_index(drop=True)

for k in tqdm(range(len(df3)), desc='{} data merge:'.format(select_file)):
    if df3['RegDt'][k].find('/') != -1:
        df3['RegDt'][k] = pd.to_datetime(df3['RegDt'][k], format='%m/%d/%y %H:%M')
    else:
        df3['RegDt'][k] = pd.to_datetime(df3['RegDt'][k], format='%Y-%m-%d %H:%M:%S')

df3 = df3.sort_values('RegDt', ascending=True).reset_index(drop=True)
df3['RegDt'] = pd.to_datetime(df3['RegDt'], format='%Y-%m-%d %H:%M:%S')

#9~11월 데이터
df3 = df3[df3['RegDt'].dt.month < 12]

df3.to_csv('data/{}.csv'.format(select_file), index=False)
print("file save: {}".format(select_file))

charger = pd.read_csv('data/' + select_file +'.csv')


# f11 = pd.read_csv('data/' + file_name1 +'.csv')
# f12 = pd.read_csv('data/' + file_name2 +'.csv')
# f13 = pd.read_csv('data/' + file_name3 +'.csv')
# f14 = pd.read_csv('data/' + file_name4 +'.csv')
# f15 = pd.read_csv('data/' + file_name5 +'.csv')

