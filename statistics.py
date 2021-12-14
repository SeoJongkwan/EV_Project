import pandas as pd
import os
import argparse
from datetime import datetime
from dateutil.relativedelta import relativedelta

from common import Data         #common class

pd.set_option('mode.chained_assignment', None)

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()

def convert_datetime(df):
    try:
        datetime.strptime(df['RegDt'][0], '%Y-%m-%d %H:%M:%S')
        df['RegDt'] = pd.to_datetime(df['RegDt'], format='%Y-%m-%d %H:%M:%S')
        return df
    except ValueError:
        print("datetime format --> %Y-%m-%d %H:%M:%S")
        datetime.strptime(df['RegDt'][0], '%m/%d/%y %H:%M')
        df['RegDt'] = pd.to_datetime(df['RegDt'], format='%m/%d/%y %H:%M')
        return df


# user_file = pd.read_csv(file_path + '_user.csv', encoding='UTF8')
# user_file['start'] = pd.to_datetime(user_file['start'], format='%Y-%m-%d %H:%M:%S')

def check_nan_value(df):
    print('Check NAN Value on Each Column:\n{}'.format(df.isnull().sum()))
    series = df.isnull().sum()
    for value in series.values:
        if value != 0:
            df1 = df[df.isnull().any(1)]
            print("NAN Value Location: {}\n{}".format(len(df1), df['RegDt'][df1.index]))
            df1 = df.drop(df1.index).reset_index(drop=True)
            return df1
    return df

def sequence_mt(f):
    file1 = f.copy()
    file1['msg'] = file1['msg'].str.replace(' ', '')

    mt = []
    for type in file1['msg']:
        mt.append(type[18:20])
    file1['mt'] = mt

    msg_type = file.msg_type()
    exp = []
    file1['exp'] = None
    for k in range(len(file1['mt'])):
        if file1['mt'][k] not in msg_type.keys():
            print("Not Defined mt:{}, index:{}".format(file1['mt'][k], k))
            file1 = file1.drop(k)
        else:
            exp.append(msg_type[file1['mt'][k]][0])
    file1['exp'] = exp
    file2 = file1[['ChargerId','RegDt','mt','exp']]
    return file2


def get_date(df, start, time, opt='day'):
    year = int(start[:4])
    month = int(start[4:6])
    day = int(start[6:8])
    hour = int(start[8:10])
    min = int(start[10:12])
    s = datetime(year, month, day, hour, min)
    if opt == 'month':
        delta = datetime(year, month, day, hour, min) + relativedelta(months=time)
        df1 = df[(df['RegDt'] > s) & (df['RegDt'] < delta)].reset_index(drop=True)
        print("duration: {} ~ {}".format(s, delta))
        return df1
    elif opt == 'day':
        delta = datetime(year, month, day, hour, min) + relativedelta(days=time)
        df1 = df[(df['RegDt'] > s) & (df['RegDt'] < delta)].reset_index(drop=True)
        print("duration: {} ~ {}".format(s, delta))
        return df1
    elif opt == 'hour':
        delta = datetime(year, month, day, hour, min) + relativedelta(hours=time)
        df1 = df[(df['RegDt'] > s) & (df['RegDt'] < delta)].reset_index(drop=True)
        print("duration: {} ~ {}".format(s, delta))
        return df1
    elif opt == 'min':
        delta = datetime(year, month, day, hour, min) + relativedelta(minutes=time)
        df1 = df[(df['RegDt'] > s) & (df['RegDt'] < delta)].reset_index(drop=True)
        print("duration: {} ~ {}".format(s, delta))
        return df1
    else:
        print("check opt select")
