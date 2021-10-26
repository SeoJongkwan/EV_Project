import pandas as pd
import os
import argparse
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from dateutil.relativedelta import relativedelta

from common import Data

pd.set_option('mode.chained_assignment', None)

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()
# print("File List: {}".format(file.file_name))
# select_file = file.file_name[2]
# print("Select File: {}".format(select_file))
# file_path = args.data_path + select_file
#
# ar_file = pd.read_csv(file_path + "_ar.csv")
# ar_cols = ['RegDt','ServerId','ChargerId','AccessId','RequireCurrent','RequireWatt','ChargingTime']
# ar = ar_file[ar_cols]
# ar = ar.copy()
# ar['RegDt'] = pd.to_datetime(ar['RegDt'], format='%Y-%m-%d %H:%M:%S')
#
# dsr_file = pd.read_csv(file_path + "_dsr.csv")
# dsr_cols = ['RegDt', 'ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
# dsr = dsr_file[dsr_cols]
# dsr = dsr.copy()
# # dsr['RegDt'] = pd.to_datetime(dsr['RegDt'], format='%Y-%m-%d %H:%M:%S')
#
# csr_file = pd.read_csv(file_path + "_csr.csv")
# csr_cols = ['RegDt','ChargerId','ChargeCurrent','ChargeVoltage','InstantaneousPower','AccumulatedWatt','ChargerNumber']
# csr = csr_file[csr_cols]
# csr = csr.copy()
# csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')
#

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

# def msg_period_statistics(df, mt):
#     print("Access Request Communication\nmonthly, daily, hourly statistics\n")
#     status_df = df[df['mt'] == mt].reset_index(drop=True)
#     print("{} / mt: {}".format(status_df['exp'][0], mt))
#
#     df1 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
#     df2 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d'))['RegDt'].count())
#     df3 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%H'))['RegDt'].count())
#
#     fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
#     sns.barplot(x=df1.index, y=df1['RegDt'], color='cornflowerblue', zorder=3, ax=ax1)
#     sns.barplot(x=df2.index, y=df2['RegDt'], color='gold', zorder=3, ax=ax2)
#     sns.barplot(x=df3.index, y=df3['RegDt'], color='plum', zorder=3, ax=ax3)
#
#     ax1.set(xlabel="RegDt", ylabel="Count", title="monthly Count")
#     ax2.set(xlabel="RegDt", ylabel="Count", title="by daily Count")
#     ax3.set(xlabel="RegDt", ylabel="Count", title="by hourly Count")
#     ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
#     ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
#     ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
#     ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
#     ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
#     ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
#     ax1.grid(True, axis='y', linestyle='dashed')
#     ax2.grid(True, axis='y', linestyle='dashed')
#     ax3.grid(True, axis='y', linestyle='dashed')
#     fig.suptitle("{} - {}(0x{})".format(status_df['ChargerId'][0], status_df['exp'][0], mt))
#     plt.tight_layout()
#     plt.show()
#     return df1, df2, df3

# original_file = pd.read_csv(file_path + ".csv")
# original_file = convert_datetime(original_file)
#
# msg_sequence = sequence_mt(original_file)
# msg_sequence['mt'].unique()
# msg_sequence['exp'].value_counts().sum()

# msg_period_statistics(msg_sequence, '05')

# user_file['user'].value_counts

def show_value_cnt(df, col):
    value_count = df[col].value_counts()
    df[col].value_counts().plot(kind='bar', figsize=(15, 5))
    plt.title('{} Value Count: unique {}'.format(col, len(df[col].unique())))
    plt.grid(True, axis='y')
    plt.tight_layout()
    plt.show()
    return value_count

# show_value_cnt(user_file, 'user')


# b = user_file.groupby([user_file['user'], user_file['start'].dt.strftime('%m-%d %H')]).count()




# user_cnt = pd.DataFrame(user_file.groupby(user_file['start'].dt.strftime('%m-%d %H'))['user'].count())
# plt.figure(figsize=(15,5))
# plt.xticks(rotation=90)
# sns.barplot(x=b.index, y=b['user'], color='cornflowerblue', zorder=3)
# plt.tight_layout()
# plt.show()