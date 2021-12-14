import pandas as pd
import argparse
import os
from tqdm import tqdm

from common import Data         #common module
import statistics as stat       #statistics module

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help="path to input file")
args = parser.parse_args()

file = Data()
print("File List: {}".format(file.file_name))

#충전기 선택
select_file = file.file_name[4]
print("Select File: {}".format(select_file))
file_path = args.data_path + select_file + ".csv"

msg_type = file.msg_type()      #message type
data = file.read_file(file_path)
msg_index = file.structure()    #header, body index location in msg

#select message type
mt = '15'
dsr_mt = file.select_mt(data, mt)
# dsr_mt.to_csv(args.data_path + "dc_100kW_mt_{}.csv".format(mt), index=False)

#data name:[length, data, value_length]
dsr_struct = {'DeviceStatus':[1, '0x01', 1], 'AccessId':[1, '0x09', 4], 'ChargerNumber':[1, '0x33', 2]}

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

status_code = {'00':'Unknown','01':'Charge Ready (케이블연결)','02':'Charging','03':'System Maintenance','04':'Not Accessible',
                 '05':'Error','06':'Charging Waiting (충전중대기)','07':'Charging Finished','08':'전원 off','09':'비상버튼 작동',
                 '0A':'충전케이블 분리 (idle)','0B':'시작버튼 누름','0C':'누전차단기 작동','0D':'충전케이블 연결오류','0E':'과전류 차단',
                 '0F':'Live/Neutral 역상','1A':'Ready (B타입)','1B':'Ready (C타입)','1C':'Ready (콤보)','1D':'Ready (차데모)',
                 '1E':'Ready (AC3상)','1F':'입력 과전압','20':'입력 저전압','21':'입력 MC 오류','22':'출력 MC 오류','23':'출력누설;선간절연 이상',
                 '24':'파원모듈 이상','25':'전력계량기 오류','26':'침수 오류'}

def data_convert(df):
    pd.set_option('mode.chained_assignment', None)
    for k in range(len(df)):
        if df['DeviceStatus'][k] in status_code.keys():
            df['DeviceStatus'][k] = status_code[df['DeviceStatus'][k]]
        else:
            print('not define Device Status Code')
        df['AccessId'][k] = int((df['AccessId'][k]), 16)
    return df

print("Data Convert:\n DeviceStatus, AccessId")
data_convert(dsr_parsing)

dsr_parsing['Send'] = dsr_mt['Send'].copy()
dsr_parsing['msgId'] = dsr_mt['msgId'].copy()
dsr_parsing.insert(0, 'RegDt', dsr_mt['RegDt'].copy())

stat.convert_datetime(dsr_parsing)


save_file = select_file + "_dsr.csv"
print("Save File: {}".format(save_file))
dsr_parsing.to_csv(args.data_path + save_file, index=False)

