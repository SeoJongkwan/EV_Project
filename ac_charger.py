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

PATH = '/Users/bellk/ION/2021.양방향 정보 기반 공동주택 스마트 충전시스템 서비스 개발 및 실증/2.연구/기관/1.클린일렉스/K차져 아파트단지/'

file1 = '경산펜타힐즈푸르지오 2ch 완속 (2782, 2783) 2111.csv'
file2 = '경산펜타힐즈푸르지오 2ch 완속 (2784, 2785) 2111.csv'
file3 = '경산펜타힐즈푸르지오 2ch 완속 (2786, 2787) 2111.csv'
file4 = '경산펜타힐즈푸르지오 2ch 완속 (2788, 2789) 2111.csv'
file5 = '경산펜타힐즈푸르지오 2ch 완속 (2790, 2791) 2111.csv'
file6 = '고덕그라시움아파트 충전기이용내역 2111.csv'

gs1 = pd.read_csv(PATH + file1, encoding='UTF8')
gs2 = pd.read_csv(PATH + file2, encoding='UTF8')
gs3 = pd.read_csv(PATH + file3, encoding='UTF8')
gs4 = pd.read_csv(PATH + file3, encoding='UTF8')
gs5 = pd.read_csv(PATH + file3, encoding='UTF8')
gs_user = pd.read_csv(PATH + file6, encoding='UTF8')

gs_user.columns
col = '결제금액'
gs_user[col] = gs_user[col].astype(int)


gs_user[col].sum()
gs_user[col].unique()
gs_user[col].value_counts()
gs_user[col].value_counts().sum()