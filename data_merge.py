import pandas as pd

path = '/Users/bellk/ION/3.양방향 정보 기반 공동주택 스마트 충전시스템 서비스 개발 및 실증/2.연구/기관/1.클린일렉스/급속충전기 로그데이터 20210906-20211015/'

file10 = '인덕원IT밸리(100kW) 20210906232638-20211015103112.xlsx'
file11 = '인덕원IT밸리(100kW) 2021001000000-20211031235959.xlsx'

a10 = pd.read_excel(path + file10)
a11 = pd.read_excel(path + file11)

def filter_date(df, df1, month):
    df['RegDt'] = pd.to_datetime(df['RegDt'], format='%Y-%m-%d %H:%M:%S')
    df1['RegDt'] = pd.to_datetime(df1['RegDt'], format='%Y-%m-%d %H:%M:%S')
    df = df[df['RegDt'].dt.month == month]
    df1 = df1[df1['RegDt'].dt.month == month+1]
    df2 = pd.concat([df, df1]).reset_index(drop=True)
    return df2

file_name1 = "dc_100kW_인덕원IT밸리"
file_name2 = "dc_50kW_광주보건환경연구원"
file_name3 = "dc_50kW_국민차매매단지공항점"
file_name4 = "dc_50kW_해오름휴게소"
file_name5 = "dc_50kW_현대이엔지세종사옥"

select_file = file_name1

df2 = filter_date(a10, a11, 9)
df2.to_csv('data/{}.csv'.format(select_file), index=False)
print("file save: {}".format(select_file))

f11 = pd.read_csv('data/' + file_name1 +'.csv')
f12 = pd.read_csv('data/' + file_name2 +'.csv')
f13 = pd.read_csv('data/' + file_name3 +'.csv')
f14 = pd.read_csv('data/' + file_name4 +'.csv')
f15 = pd.read_csv('data/' + file_name5 +'.csv')

