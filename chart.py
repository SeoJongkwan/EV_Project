import matplotlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.ticker import MaxNLocator
from datetime import datetime
from dateutil.relativedelta import relativedelta

pd.set_option('mode.chained_assignment', None)

plt.rc('font', family='AppleGothic', size=10)
plt.rc('axes', unicode_minus=False)
plt.rc('xtick', labelsize=10)
plt.rc('ytick', labelsize=10)


def show_value_cnt(df, file, col):
    value_count = df[col].value_counts()
    df[col].value_counts().plot(kind='barh', color='navy', figsize=(10, 5))
    for i, v in enumerate(value_count):
        plt.text(v+10, i, str(v), fontweight='bold')
    plt.title('{} / {} Info'.format(file, col))
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


def show_device_status_ratio(file, df, min=2):
    df['percent'] = None
    for i in range(len(df)):
        s = df['DeviceStatus'].sum()
        df['percent'][i] = round((df['DeviceStatus'][i] / s)*100, 2)
        if df['percent'][i] < min:
            print("Remove ({}%) - {}: {}times / {}%".format(min, df.index[i], df['DeviceStatus'][i], df['percent'][i]))
    df1 = df[df['percent'] > min]
    wedgeprops = {'width': 0.7, 'edgecolor': 'w', 'linewidth': 5}
    colors = sns.color_palette('pastel')
    plt.pie(df1['DeviceStatus'], labels=df1.index, autopct='%.1f%%', counterclock=False, colors=colors, wedgeprops=wedgeprops)
    plt.title("{} / Device Status Ratio (>{}%)".format(file, min), fontdict={'size':'medium'})
    # plt.axis('equal')
    plt.tight_layout()
    plt.show()
    return df1


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


def show_msg_period_statistics(df, file, mt):
    print("Access Request Communication\nmonthly, daily, hourly statistics\n")
    status_df = df[df['mt'] == mt].reset_index(drop=True)
    print("{} / mt: {}".format(status_df['exp'][0], mt))

    df1 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m'))['RegDt'].count())
    df2 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%m-%d'))['RegDt'].count())
    df3 = pd.DataFrame(status_df.groupby(status_df['RegDt'].dt.strftime('%H'))['RegDt'].count())

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8))
    sns.barplot(x=df1.index, y=df1['RegDt'], color='cornflowerblue', zorder=3, ax=ax1)
    sns.barplot(x=df2.index, y=df2['RegDt'], color='gold', zorder=3, ax=ax2)
    sns.barplot(x=df3.index, y=df3['RegDt'], color='plum', zorder=3, ax=ax3)

    ax1.set(xlabel="RegDt", ylabel="Count", title="monthly Count")
    ax2.set(xlabel="RegDt", ylabel="Count", title="by daily Count")
    ax3.set(xlabel="RegDt", ylabel="Count", title="by hourly Count")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
    ax1.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax2.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax3.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax1.grid(True, axis='y', linestyle='dashed')
    ax2.grid(True, axis='y', linestyle='dashed')
    ax3.grid(True, axis='y', linestyle='dashed')
    fig.suptitle("{}({}) / {}".format(file, status_df['ChargerId'][0], status_df['exp'][0]))
    plt.tight_layout()
    plt.show()
    return df1, df2, df3



