import pandas as pd
import argparse
import os
from tqdm import tqdm

from common import Data         #common module
import statistics as stat       #statistics module

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
mt = '1B'
csr_ack_mt = file.select_mt(data, mt)

#data name:[length, data, value_length]
csr_ack_struct = {'MessagePending':[1, '0x12', 1], 'RequireWatt':[1, '0x17', 3], 'WakeupInterval':[1, '0x13', 1], 'ChargingFee':[1, '28', 5], 'ChargerNumber':[1, '33', 2]}

def msg_parsing(df):
    ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
    MessagePending_type, RequireWatt_type, WakeupInterval_type, ChargingFee_type, ChargerNumber_type = [], [], [], [], []
    MessagePending, RequireWatt, WakeupInterval, ChargingFee, ChargerNumber = [], [], [], [], []

    for i in tqdm(df.index, desc='Extract header&body'):
        ServerId.append(df['msg'][i][0:msg_index[0]])
        ChargerId.append(df['msg'][i][msg_index[0]:msg_index[1]])
        Length.append(df['msg'][i][msg_index[1]:msg_index[2]])
        MessageType.append(df['msg'][i][msg_index[2]:msg_index[3]])
        SequenceNumber.append(df['msg'][i][msg_index[3]:msg_index[4]])
        DataLength.append(df['msg'][i][msg_index[4]:msg_index[5]])

        MessagePending_type_index = msg_index[5] + csr_ack_struct['MessagePending'][0] * 2
        MessagePending_type.append(df['msg'][i][msg_index[5]:MessagePending_type_index])
        MessagePending_value_index = MessagePending_type_index + csr_ack_struct['MessagePending'][2] * 2
        MessagePending.append(df['msg'][i][MessagePending_type_index:MessagePending_value_index])

        RequireWatt_type_index = MessagePending_value_index + csr_ack_struct['RequireWatt'][0] * 2
        RequireWatt_type.append(df['msg'][i][MessagePending_value_index:RequireWatt_type_index])
        RequireWatt_value_index = RequireWatt_type_index + csr_ack_struct['RequireWatt'][2] * 2
        RequireWatt.append(df['msg'][i][RequireWatt_type_index:RequireWatt_value_index])

        WakeupInterval_type_index = RequireWatt_value_index + csr_ack_struct['WakeupInterval'][0] * 2
        WakeupInterval_type.append(df['msg'][i][RequireWatt_value_index:WakeupInterval_type_index])
        WakeupInterval_value_index = WakeupInterval_type_index + csr_ack_struct['WakeupInterval'][2] * 2
        WakeupInterval.append(df['msg'][i][WakeupInterval_type_index:WakeupInterval_value_index])

        ChargingFee_type_index = WakeupInterval_value_index + csr_ack_struct['ChargingFee'][0] * 2
        ChargingFee_type.append(df['msg'][i][WakeupInterval_value_index:ChargingFee_type_index])
        ChargingFee_value_index = ChargingFee_type_index + csr_ack_struct['ChargingFee'][2] * 2
        ChargingFee.append(df['msg'][i][ChargingFee_type_index:ChargingFee_value_index])

        ChargerNumber_type_index = ChargingFee_value_index + csr_ack_struct['ChargerNumber'][0] * 2
        ChargerNumber_type.append(df['msg'][i][ChargingFee_value_index:ChargerNumber_type_index])
        ChargerNumber_value_index = ChargerNumber_type_index + csr_ack_struct['ChargerNumber'][2] * 2
        ChargerNumber.append(df['msg'][i][ChargerNumber_type_index:ChargerNumber_value_index])

    df_original = pd.DataFrame(
        {'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType, 'SequenceNumber': SequenceNumber,
         'DataLength': DataLength, 'MessagePending_type': MessagePending_type, 'MessagePending': MessagePending, 'RequireWatt_type': RequireWatt_type,
         'RequireWatt': RequireWatt, 'WakeupInterval_type': WakeupInterval_type, 'WakeupInterval': WakeupInterval, 'ChargingFee_type': ChargingFee_type,
         'ChargingFee': ChargingFee, 'ChargerNumber_type': ChargerNumber_type, 'ChargerNumber': ChargerNumber
         })

    return df_original

csr_ack_original = msg_parsing(csr_ack_mt)
csr_ack_parsing = csr_ack_original.copy()

def data_convert(df):
    mp = []
    for k in df['MessagePending'].to_numpy():
        mp.append(int([k][0], 16))
    df['MessagePending'] = mp
    rw = []
    for k in df['RequireWatt'].to_numpy():
        rw.append(int([k][0], 16))
    df['RequireWatt'] = rw
    cf = []
    for k in df['ChargingFee'].to_numpy():
        cf.append(bytes.fromhex([k][0]).decode())
    df['ChargingFee'] = cf
    return df

print("Data Convert:\n MessagePending, MessagePending, RequireWatt, ChargingFee")
data_convert(csr_ack_parsing)

csr_ack_parsing['ServerId'] = csr_ack_original['ServerId'].copy()
csr_ack_parsing['Send'] = csr_ack_mt['Send'].copy()
csr_ack_parsing['msgId'] = csr_ack_mt['msgId'].copy()
csr_ack_parsing.insert(0, 'RegDt', csr_ack_mt['RegDt'].copy())

stat.convert_datetime(csr_ack_parsing)

save_file = select_file + "_csr_ack.csv"
print("Save File: {}".format(save_file))
csr_ack_parsing.to_csv(args.data_path + save_file, index=False)
