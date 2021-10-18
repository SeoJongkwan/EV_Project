import pandas as pd
import argparse
import os
from tqdm import tqdm

import statistics as stat       #statistics module
from common import Data         #common module

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()
print("File List: {}".format(file.file_name))
select_file = file.file_name[4]
print("Select File: {}".format(select_file))
file_path = args.data_path + select_file + ".csv"

msg_type = file.msg_type()      #message type
data = file.read_file(file_path)
msg_index = file.structure()    #header, body index location in msg

#select message type
mt = '05'
ar_mt = file.select_mt(data, mt)

#data name:[length, data, value_length]
ar_struct = {'AccessId':[1,'0x09',4],'RequireCurrent':[1,'0x18',1],'RequireWatt':[1,'0x20',3],
            'ChargingTime':[1,'0x06',2],'StartDelay':[1,'0x07',2],'UserConfirm':[1,'0x26',1],'ChargerNumber':[1,'0x33',2]}


def msg_parsing(df):
    ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
    AccessId_type, RequireCurrent_type, RequireWatt_type, ChargingTime_type, StartDelay_type, UserConfirm_type, ChargerNumber_type = [], [], [], [], [], [], []
    AccessId, RequireCurrent, RequireWatt, ChargingTime, StartDelay, UserConfirm, ChargerNumber = [], [], [], [], [], [], []

    for i in tqdm(df.index, desc='Extract header&body'):
        ServerId.append(df['msg'][i][0:msg_index[0]])
        ChargerId.append(df['msg'][i][msg_index[0]:msg_index[1]])
        Length.append(df['msg'][i][msg_index[1]:msg_index[2]])
        MessageType.append(df['msg'][i][msg_index[2]:msg_index[3]])
        SequenceNumber.append(df['msg'][i][msg_index[3]:msg_index[4]])
        DataLength.append(df['msg'][i][msg_index[4]:msg_index[5]])

        AccessId_type_index = msg_index[5] + ar_struct['AccessId'][0] * 2
        AccessId_type.append(df['msg'][i][msg_index[5]:AccessId_type_index])
        AccessId_value_index = AccessId_type_index + ar_struct['AccessId'][2] * 2
        AccessId.append(df['msg'][i][AccessId_type_index:AccessId_value_index])

        RequireCurrent_type_index = AccessId_value_index + ar_struct['RequireCurrent'][0] * 2
        RequireCurrent_type.append(df['msg'][i][AccessId_value_index:RequireCurrent_type_index])
        RequireCurrent_value_index = RequireCurrent_type_index + ar_struct['RequireCurrent'][2] * 2
        RequireCurrent.append(df['msg'][i][RequireCurrent_type_index:RequireCurrent_value_index])

        RequireWatt_type_index = RequireCurrent_value_index + ar_struct['RequireWatt'][0] * 2
        RequireWatt_type.append(df['msg'][i][RequireCurrent_value_index:RequireWatt_type_index])
        RequireWatt_value_index = RequireWatt_type_index + ar_struct['RequireWatt'][2] * 2
        RequireWatt.append(df['msg'][i][RequireWatt_type_index:RequireWatt_value_index])

        ChargingTime_type_index = RequireWatt_value_index + ar_struct['ChargingTime'][0] * 2
        ChargingTime_type.append(df['msg'][i][RequireWatt_value_index:ChargingTime_type_index])
        ChargingTime_value_index = ChargingTime_type_index + ar_struct['ChargingTime'][2] * 2
        ChargingTime.append(df['msg'][i][ChargingTime_type_index:ChargingTime_value_index])

        StartDelay_type_index = ChargingTime_value_index + ar_struct['StartDelay'][0] * 2
        StartDelay_type.append(df['msg'][i][ChargingTime_value_index:StartDelay_type_index])
        StartDelay_value_index = StartDelay_type_index + ar_struct['StartDelay'][2] * 2
        StartDelay.append(df['msg'][i][StartDelay_type_index:StartDelay_value_index])

        UserConfirm_type_index = StartDelay_value_index + ar_struct['UserConfirm'][0] * 2
        UserConfirm_type.append(df['msg'][i][StartDelay_value_index:UserConfirm_type_index])
        UserConfirm_value_index = UserConfirm_type_index + ar_struct['UserConfirm'][2] * 2
        UserConfirm.append(df['msg'][i][UserConfirm_type_index:UserConfirm_value_index])

        ChargerNumber_type_index = UserConfirm_value_index + ar_struct['ChargerNumber'][0] * 2
        ChargerNumber_type.append(df['msg'][i][UserConfirm_value_index:ChargerNumber_type_index])
        ChargerNumber_value_index = ChargerNumber_type_index + ar_struct['ChargerNumber'][2] * 2
        ChargerNumber.append(df['msg'][i][ChargerNumber_type_index:ChargerNumber_value_index])

    df_original = pd.DataFrame(
        {'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType, 'SequenceNumber': SequenceNumber,
         'DataLength': DataLength, 'AccessId_type': AccessId_type, 'AccessId': AccessId, 'RequireCurrent_type': RequireCurrent_type,
         'RequireCurrent': RequireCurrent, 'RequireWatt_type': RequireWatt_type, 'RequireWatt': RequireWatt, 'ChargingTime_type': ChargingTime_type,
         'ChargingTime': ChargingTime, 'StartDelay_type': StartDelay_type, 'StartDelay': StartDelay, 'UserConfirm_type': UserConfirm_type,
         'UserConfirm': UserConfirm, 'ChargerNumber_type': ChargerNumber_type, 'ChargerNumber': ChargerNumber
         })

    return df_original

ar_original = msg_parsing(ar_mt)
ar_parsing = ar_original.copy()

def data_convert(df):
    pd.set_option('mode.chained_assignment', None)
    for k in range(len(df)):
        df['AccessId'][k] = int((df['AccessId'][k]), 16)
    rw = []
    for k in df['RequireWatt'].to_numpy():
        rw.append(int([k][0], 16) * 10 / 1000)  # 1000mWh
    df['RequireWatt'] = rw
    ct = []
    for k in df['ChargingTime'].to_numpy():
        ct.append(int([k][0], 16))
    df['ChargingTime'] = ct
    sd = []
    for k in df['StartDelay'].to_numpy():
        sd.append(int([k][0], 16))
    df['StartDelay'] = sd
    return df

print("Data Convert:\n AccessId, RequireCurrent, RequireWatt, ChargingTime, StartDelay")
ar_parsing = data_convert(ar_parsing)

ar_parsing.insert(0, 'RegDt', ar_mt['RegDt'].copy())
stat.convert_datetime(ar_parsing)

save_file = select_file + "_ar.csv"
print("Save File: {}".format(save_file))
ar_parsing.to_csv(args.data_path + save_file, index=False)

