import pandas as pd
import argparse
import os
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
from common import Data         #common class

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file_name = "dc_100kW.csv"
file = Data(args.data_path + file_name)
msg_type = file.msg_type()      #message type
data = file.read_file()
msg_index = file.structure()    #header, body index location in msg

#select message type
mt = '15'
dsr_mt = file.select_mt(data, mt)
dsr_mt.to_csv(args.data_path + "dc_100kW_mt_{}.csv".format(mt), index=False)

#data name:[length, data, value_length]
dsr_struct = {'DeviceStatus':[1, '0x01', 1], 'AccessId':[1, '0x09', 4], 'ChargerNumber':[1, '33', 2]}

def msg_parsing(df):
    ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
    DeviceStatus_type, AccessId_type, ChargerNumber_type = [], [], []
    DeviceStatus, AccessId, ChargerNumber = [], [], []

    for i in tqdm(df.index, desc='Extract header & body'):
        ServerId.append(df['msg'][i][0:msg_index[0]])
        ChargerId.append(df['msg'][i][msg_index[0]:msg_index[1]])
        Length.append(df['msg'][i][msg_index[1]:msg_index[2]])
        MessageType.append(df['msg'][i][msg_index[2]:msg_index[3]])
        SequenceNumber.append(df['msg'][i][msg_index[3]:msg_index[4]])
        DataLength.append(df['msg'][i][msg_index[4]:msg_index[5]])

        DeviceStatus_type_index = msg_index[5] + dsr_struct['DeviceStatus'][0] * 2
        DeviceStatus_type.append(df['msg'][i][msg_index[5]:DeviceStatus_type_index])
        DeviceStatus_value_index = DeviceStatus_type_index + dsr_struct['DeviceStatus'][2] * 2
        DeviceStatus.append(df['msg'][i][DeviceStatus_type_index:DeviceStatus_value_index])

        AccessId_type_index = DeviceStatus_value_index + dsr_struct['AccessId'][0] * 2
        AccessId_type.append(df['msg'][i][DeviceStatus_value_index:AccessId_type_index])
        AccessId_value_index = AccessId_type_index + dsr_struct['AccessId'][2] * 2
        AccessId.append(df['msg'][i][AccessId_type_index:AccessId_value_index])

        ChargerNumber_type_index = AccessId_value_index + dsr_struct['ChargerNumber'][0] * 2
        ChargerNumber_type.append(df['msg'][i][AccessId_value_index:ChargerNumber_type_index])
        ChargerNumber_value_index = ChargerNumber_type_index + dsr_struct['ChargerNumber'][2] * 2
        ChargerNumber.append(df['msg'][i][ChargerNumber_type_index:ChargerNumber_value_index])

    df_original = pd.DataFrame(
        {'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType, 'SequenceNumber': SequenceNumber,
         'DataLength': DataLength, 'DeviceStatus_type': DeviceStatus_type, 'DeviceStatus': DeviceStatus, 'AccessId_type': AccessId_type,
         'AccessId': AccessId, 'ChargerNumber_type': ChargerNumber_type, 'ChargerNumber': ChargerNumber
         })

    return df_original

dsr_original = msg_parsing(dsr_mt)
dsr_parsing = dsr_original.copy()

def data_convert(target, df):
    pd.set_option('mode.chained_assignment', None)
    for k in range(len(df)):
        df['AccessId'][k] = int((target['AccessId'][k]), 16)

data_convert(dsr_original, dsr_parsing)

dsr_parsing['RegDt'] = dsr_mt['RegDt'].copy()
dsr_parsing['RegDt'] = pd.to_datetime(dsr_parsing['RegDt'], format='%Y-%m-%d %H:%M:%S')
dsr_parsing['Send'] = dsr_mt['Send'].copy()
dsr_parsing['msgId'] = dsr_mt['msgId'].copy()
dsr_parsing.to_csv(args.data_path + "dc_100kW_dsr.csv", index=False)

dsr_done = pd.read_csv(args.data_path + "dc_100kW_dsr.csv", dtype='str')
select_cols = ['RegDt','ChargerId', 'DeviceStatus', 'AccessId', 'ChargerNumber']
dsr = dsr_done[select_cols]


# dsr_original.dtypes
# csr_ack.columns
# csr_ack.dtypes
# csr_ack.describe()
#
# csr_ack.ChargerId.value_counts()
# csr_ack.ChargerId.nunique()
#
# plt.plot(csr_ack["RegDt"], csr_ack["RequireWatt"])
# sns.distplot(csr_ack["RequireWatt"])
# plt.show()
