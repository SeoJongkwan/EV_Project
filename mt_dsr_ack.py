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
mt = '1A'
dsr_ack_mt = file.select_mt(data, mt)
dsr_ack_mt.to_csv(args.data_path + "dc_100kW_mt_{}.csv".format(mt), index=False)

#data name:[length, data, value_length]
dsr_ack_struct = {'MessagePending':[1, '0x12', 1], 'WakeupInterval':[1, '0x13', 1], 'ChargerNumber':[1, '33', 2]}

def msg_parsing(df):
    ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
    MessagePending_type, WakeupInterval_type, ChargerNumber_type = [], [], []
    MessagePending, WakeupInterval, ChargerNumber = [], [], []

    for i in tqdm(df.index, desc='Extract header&body'):
        ServerId.append(df['msg'][i][0:msg_index[0]])
        ChargerId.append(df['msg'][i][msg_index[0]:msg_index[1]])
        Length.append(df['msg'][i][msg_index[1]:msg_index[2]])
        MessageType.append(df['msg'][i][msg_index[2]:msg_index[3]])
        SequenceNumber.append(df['msg'][i][msg_index[3]:msg_index[4]])
        DataLength.append(df['msg'][i][msg_index[4]:msg_index[5]])

        MessagePending_type_index = msg_index[5] + dsr_ack_struct['MessagePending'][0] * 2
        MessagePending_type.append(df['msg'][i][msg_index[5]:MessagePending_type_index])
        MessagePending_value_index = MessagePending_type_index + dsr_ack_struct['MessagePending'][2] * 2
        MessagePending.append(df['msg'][i][MessagePending_type_index:MessagePending_value_index])

        WakeupInterval_type_index = MessagePending_value_index + dsr_ack_struct['WakeupInterval'][0] * 2
        WakeupInterval_type.append(df['msg'][i][MessagePending_value_index:WakeupInterval_type_index])
        WakeupInterval_value_index = WakeupInterval_type_index + dsr_ack_struct['WakeupInterval'][2] * 2
        WakeupInterval.append(df['msg'][i][WakeupInterval_type_index:WakeupInterval_value_index])

        ChargerNumber_type_index = WakeupInterval_value_index + dsr_ack_struct['ChargerNumber'][0] * 2
        ChargerNumber_type.append(df['msg'][i][WakeupInterval_value_index:ChargerNumber_type_index])
        ChargerNumber_value_index = ChargerNumber_type_index + dsr_ack_struct['ChargerNumber'][2] * 2
        ChargerNumber.append(df['msg'][i][ChargerNumber_type_index:ChargerNumber_value_index])

    df_original = pd.DataFrame(
        {'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType, 'SequenceNumber': SequenceNumber,
         'DataLength': DataLength, 'MessagePending_type': MessagePending_type, 'MessagePending': MessagePending, 'WakeupInterval_type': WakeupInterval_type,
         'WakeupInterval': WakeupInterval, 'ChargerNumber_type': ChargerNumber_type, 'ChargerNumber': ChargerNumber
         })

    return df_original

dsr_ack_original = msg_parsing(dsr_ack_mt)
dsr_ack_parsing = dsr_ack_original.copy()

def data_convert(target, df):
    mp = []
    for k in df['MessagePending'].to_numpy():
        mp.append(int([k][0], 16))
    df['MessagePending'] = mp

data_convert(dsr_ack_original, dsr_ack_parsing)

dsr_ack_parsing['ServerId'] = dsr_ack_original['ServerId'].copy()
dsr_ack_parsing['Send'] = dsr_ack_mt['Send'].copy()
dsr_ack_parsing['msgId'] = dsr_ack_mt['msgId'].copy()
dsr_ack_parsing.insert(0, 'RegDt', dsr_ack_mt['RegDt'].copy())
dsr_ack_parsing['RegDt'] = pd.to_datetime(dsr_ack_mt['RegDt'], format='%Y-%m-%d %H:%M:%S')
dsr_ack_parsing.to_csv(args.data_path + "dc_100kW_dsr_ack.csv", index=False)

dsr_ack_done = pd.read_csv(args.data_path + "dc_100kW_dsr_ack.csv", dtype='str')
select_cols = ['RegDt','ChargerId', 'MessagePending', 'WakeupInterval', 'ChargerNumber']
dsr_ack = dsr_ack_done[select_cols]

# dsr_ack_parsing.info()
