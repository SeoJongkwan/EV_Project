import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams["font.family"] = "NanumBarunGothic"

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
    plt.title('{} Value Count'.format(col))
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.show()
    return value_count

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

