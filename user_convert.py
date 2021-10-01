import pandas as pd
import numpy as np
import argparse
import os
import datetime

pd.set_option('mode.chained_assignment', None) # SettingWithCopyWarning

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

original_file = 'dc_100kW_user_original.csv'
user_file = pd.read_csv(args.data_path + original_file, encoding='UTF8')
print("original file:", original_file)

print("\ncolumn name change: kor --> eng")
user_col = ['SID', 'time', 'charger', 'AS', 'chargerNo', 'user', 'carNo', 'duration', 'AccumulatedWatt',
            'chargingFee', 'payment', 'payMethod', 'roaming', 'roamingNo', 'status', 'chargerStatus']
user_file.columns = user_col

print('time column split --> start & end')
user_file.insert(1, 'start', user_file['time'].str.split('~').str[0])
user_file.insert(2, 'end', user_file['time'].str.split('~').str[1])
user_file['start'] = user_file['start'].str.rstrip()
user_file['start'] = pd.to_datetime(user_file['start'], format='%y/%m/%d %H:%M')
user_file['end'] = user_file['end'].str.lstrip()
user_file['end'] = pd.to_datetime(user_file['end'], format='%y/%m/%d %H:%M')

# user_file['start'] = user_file['start'].dt.strftime('%Y-%m-%d %H:%M')
# user_file['end'] = user_file['end'].dt.strftime('%Y-%m-%d %H:%M')

print('duration(h:m:s) column transform --> second')
user_file['second'] = 0
user_file['minute'] = 0
user_file['hour'] = 0

user_file['duration'].str.strip()
for i in range(len(user_file)):
    locate = user_file['duration'][i].find('초')
    if locate != -1:
        user_file['second'][i] = int(user_file['duration'][i][locate - 3:locate])
    else:
        pass

for i in range(len(user_file)):
    locate = user_file['duration'][i].find('분')
    if locate != -1:
        if locate > 2:
            user_file['minute'][i] = int(user_file['duration'][i][locate - 3:locate]) * 60
        else:
            user_file['minute'][i] = int(user_file['duration'][i][:locate].rstrip()) * 60
    else:
        pass

for i in range(len(user_file)):
    locate = user_file['duration'][i].find('시간')
    if locate != -1:
        if locate > 2:
            user_file['hour'][i] = int(user_file['duration'][i][locate - 3:locate]) * 3600
        else:
            user_file['hour'][i] = int(user_file['duration'][i][:locate].rstrip()) * 3600
    else:
        pass

for i in range(len(user_file)):
    user_file['duration'][i] = user_file['hour'][i]+user_file['minute'][i]+user_file['second'][i]

drop_col = ['time','hour','minute','second']
user_file = user_file.drop(drop_col, axis=1)
print("drop columns", drop_col)
user_file = user_file.sort_values(by='start',ascending=True).reset_index(drop=True)

transform_file = 'dc_100kW_user.csv'
print("\ntransform file:", transform_file)
user_file.to_csv(args.data_path + transform_file, index=False)

