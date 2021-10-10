import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from dateutil.relativedelta import relativedelta

plt.rc('font', family='AppleGothic', size=10)
plt.rc('axes', unicode_minus=False)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)

def check_nan_value(df):
    '''
    :param df: NAN value check
    :return: df except NAN value
    '''
    print('Check NAN Value on Each Column:\n{}'.format(df.isnull().sum()))
    series = df.isnull().sum()
    for value in series.values:
        if value != 0:
            df1 = df[df.isnull().any(1)]
            print("NAN Value Location: {}\n{}".format(len(df1), df['RegDt'][df1.index]))
            df1 = df.drop(df1.index).reset_index(drop=True)
            return df1
    return df

def show_value_cnt(df, col):
    '''
    :param df: field unique value count
    :param col: selection field
    :return: series&chart field unique value count
    '''
    value_count = df[col].value_counts()
    df[col].value_counts().plot(kind='barh', figsize=(10, 5))
    for i, v in enumerate(value_count):
        plt.text(v+10, i, str(v), fontweight='bold')
    start = str(df.iloc[0, 0])[:-9]
    end = str(df.iloc[-1, 0])[:-9]
    plt.title('{} Value Count: {} ~ {}'.format(col, start, end))
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.show()
    return value_count

def show_device_status(df, status):
    status_df = df[df['DeviceStatus']==status].reset_index(drop=True)
    print("-DeviceStatus:", status)
    print("-ChargerNumber:", status_df['ChargerNumber'].unique())
    cnt = status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d %H:%M'))['RegDt'].count()
    cnt1 = cnt.to_frame(name="count")
    cnt2 = cnt1.reset_index()
    ax = cnt1.plot(kind='bar', figsize=(7, 3), zorder=3, color='gold')
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.get_legend().remove()
    plt.title("Count Device Status: {} / {} times".format(status, len(cnt1)), fontdict={'size':'medium'})
    plt.xticks(fontsize=7)
    plt.yticks(fontsize=7)
    plt.xlabel("RegDt", fontdict={'size':'small'})
    plt.ylabel("count", fontdict={'size':'small'})
    plt.grid(True, axis='y', linestyle='dashed')
    plt.tight_layout()
    plt.show()
    return cnt2


def show_feature_correlation(df, time, col):
    plt.style.use('dark_background')
    df = df.set_index(time)
    corr = df.corr(method='pearson')
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    mask[:,2]
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(20,10))
    # fig, ax1 = plt.subplots(1,1, figsize=(10, 6))
    sns.heatmap(data=corr, mask=mask, annot=True, fmt='.2f', linewidths=.5, cmap ='Blues', vmin = -1, vmax = 1, ax=ax1)
    buttom, top = ax1.get_ylim(); ax1.set_ylim(buttom+0.5, top-0.5)
    ax1.set(title='Feature Correlation')

    df_cor = corr.sort_values(col, axis=0, ascending=False)
    df_cor[col].plot(kind='bar', color='cyan', ax=ax2)
    ax2.set(ylabel='coefficient', title='Feature Importance')
    plt.style.use('dark_background')
    plt.tight_layout()
    plt.show()

def show_feature_importance(df, time, col):
    plt.style.use('dark_background')
    df = df.set_index(time)
    corr = df.corr(method='pearson')
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    mask[:,2]
    fig, ax1 = plt.subplots(1,1,figsize=(12,8))

    df_cor = corr.sort_values(col, axis=0, ascending=False)
    df_cor[col].plot(kind='bar', color='cyan', ax=ax1)
    ax1.set(ylabel='coefficient', title='Feature Importance')
    plt.tight_layout()
    plt.show()

def show_variable_relation(df, time, col1, col2):
    fig, ax1 = plt.subplots(figsize=(18,6))
    sns.lineplot(df[time], df[col1], label=col1, color='plum', ax=ax1)
    ax1.set(xlabel=col2, ylabel=col1, title='{} & {} Relation'.format(col1, col2)), ax1.legend(loc=2)
    ax2 = ax1.twinx()
    sns.lineplot(df[time], df[col2], label=col2, color='gold', ax=ax2), ax2.legend(loc=1)
    plt.tight_layout()
    plt.show()


def show_density(df, col):
    fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw={"height_ratios": (.15, .85)}, figsize=(18,4))
    sns.boxplot(df[col], ax=ax1)
    sns.distplot(df[col], norm_hist=True, ax=ax2)
    ax1.set(xlabel='')
    ax2.set(xlabel=col, ylabel='density', title='{} Disribution Density'.format(col))
    plt.tight_layout()
    plt.show()


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
