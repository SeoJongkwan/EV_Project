import pandas as pd
import argparse
import os
from tqdm import tqdm
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
mt = '16'
csr_mt = file.select_mt(data, mt)
# csr_mt.to_csv(args.data_path + "dc_100kW_mt_{}.csv".format(mt), index=False)

#data name:[length, data, value_length]
csr_struct = {'ChargeCurrent':[1,'0x02',2],'ChargeVoltage':[1,'0x03',2],'Temperature':[1,'0x04',1],
            'AccumulatedWatt':[1,'05',3],'AccessId':[1,'0x09',4],'ElaspedTime':[1,'0A',3],'ChargerNumber':[1,'33',2]}

def msg_parsing(df):
    ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
    ChargeCurrent_type, ChargeVoltage_type, Temperature_type, AccumulatedWatt_type, AccessId_type, ElaspedTime_type, ChargerNumber_type = [], [], [], [], [], [], []
    ChargeCurrent, ChargeVoltage, Temperature, AccumulatedWatt, AccessId, ElaspedTime, ChargerNumber = [], [], [], [], [], [], []

    for i in tqdm(df.index, desc='Extract header&body'):
        ServerId.append(df['msg'][i][0:msg_index[0]])
        ChargerId.append(df['msg'][i][msg_index[0]:msg_index[1]])
        Length.append(df['msg'][i][msg_index[1]:msg_index[2]])
        MessageType.append(df['msg'][i][msg_index[2]:msg_index[3]])
        SequenceNumber.append(df['msg'][i][msg_index[3]:msg_index[4]])
        DataLength.append(df['msg'][i][msg_index[4]:msg_index[5]])

        ChargeCurrent_type_index = msg_index[5] + csr_struct['ChargeCurrent'][0] * 2
        ChargeCurrent_type.append(df['msg'][i][msg_index[5]:ChargeCurrent_type_index])
        ChargeCurrent_value_index = ChargeCurrent_type_index + csr_struct['ChargeCurrent'][2] * 2
        ChargeCurrent.append(df['msg'][i][ChargeCurrent_type_index:ChargeCurrent_value_index])

        ChargeVoltage_type_index = ChargeCurrent_value_index + csr_struct['ChargeVoltage'][0] * 2
        ChargeVoltage_type.append(df['msg'][i][ChargeCurrent_value_index:ChargeVoltage_type_index])
        ChargeVoltage_value_index = ChargeVoltage_type_index + csr_struct['ChargeVoltage'][2] * 2
        ChargeVoltage.append(df['msg'][i][ChargeVoltage_type_index:ChargeVoltage_value_index])

        Temperature_type_index = ChargeVoltage_value_index + csr_struct['Temperature'][0] * 2
        Temperature_type.append(df['msg'][i][ChargeVoltage_value_index:Temperature_type_index])
        Temperature_value_index = Temperature_type_index + csr_struct['Temperature'][2] * 2
        Temperature.append(df['msg'][i][Temperature_type_index:Temperature_value_index])

        AccumulatedWatt_type_index = Temperature_value_index + csr_struct['AccumulatedWatt'][0] * 2
        AccumulatedWatt_type.append(df['msg'][i][Temperature_value_index:AccumulatedWatt_type_index])
        AccumulatedWatt_value_index = AccumulatedWatt_type_index + csr_struct['AccumulatedWatt'][2] * 2
        AccumulatedWatt.append(df['msg'][i][AccumulatedWatt_type_index:AccumulatedWatt_value_index])

        AccessId_type_index = AccumulatedWatt_value_index + csr_struct['AccessId'][0] * 2
        AccessId_type.append(df['msg'][i][AccumulatedWatt_value_index:AccessId_type_index])
        AccessId_value_index = AccessId_type_index + csr_struct['AccessId'][2] * 2
        AccessId.append(df['msg'][i][AccessId_type_index:AccessId_value_index])

        ElaspedTime_type_index = AccessId_value_index + csr_struct['ElaspedTime'][0] * 2
        ElaspedTime_type.append(df['msg'][i][AccessId_value_index:ElaspedTime_type_index])
        ElaspedTime_value_index = ElaspedTime_type_index + csr_struct['ElaspedTime'][2] * 2
        ElaspedTime.append(df['msg'][i][ElaspedTime_type_index:ElaspedTime_value_index])

        ChargerNumber_type_index = ElaspedTime_value_index + csr_struct['ChargerNumber'][0] * 2
        ChargerNumber_type.append(df['msg'][i][ElaspedTime_value_index:ChargerNumber_type_index])
        ChargerNumber_value_index = ChargerNumber_type_index + csr_struct['ChargerNumber'][2] * 2
        ChargerNumber.append(df['msg'][i][ChargerNumber_type_index:ChargerNumber_value_index])

    df_original = pd.DataFrame(
        {'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType, 'SequenceNumber': SequenceNumber,
         'DataLength': DataLength, 'ChargeCurrent_type': ChargeCurrent_type, 'ChargeCurrent': ChargeCurrent, 'ChargeVoltage_type': ChargeVoltage_type,
         'ChargeVoltage': ChargeVoltage, 'Temperature_type': Temperature_type, 'Temperature': Temperature, 'AccumulatedWatt_type': AccumulatedWatt_type,
         'AccumulatedWatt': AccumulatedWatt, 'AccessId_type': AccessId_type, 'AccessId': AccessId, 'ElaspedTime_type': ElaspedTime_type,
         'ElaspedTime': ElaspedTime, 'ChargerNumber_type': ChargerNumber_type, 'ChargerNumber': ChargerNumber
         })

    return df_original

csr_original = msg_parsing(csr_mt)
csr_parsing = csr_original.copy()

def data_convert(target, df):
    pd.set_option('mode.chained_assignment', None)
    cc = []
    for k in df['ChargeCurrent'].to_numpy():
        cc.append(int([k][0], 16) * 10 / 1000)       #10mA
    df['ChargeCurrent'] = cc
    cv = []
    for k in df['ChargeVoltage'].to_numpy():
        cv.append(int([k][0], 16) * 10 / 1000)       #100mV
    df['ChargeVoltage'] = cv
    aw = []
    for k in df['AccumulatedWatt'].to_numpy():
        aw.append(int([k][0], 16) * 10 / 1000)       #1000mWh
    df['AccumulatedWatt'] = aw
    for k in range(len(df)):
        df['AccessId'][k] = int((df['AccessId'][k]), 16)
    #ElaspedTime: HH:MM:SS
    for j in tqdm(range(len(target)), desc='ElaspedTime Transform'):
        df['ElaspedTime'][j] = [target['ElaspedTime'][j][i:i + 2] for i in range(0, len(target['ElaspedTime'][j]), 2)]
        for c in range(len(df['ElaspedTime'][j])):
            df['ElaspedTime'][j][c] = str(int((df['ElaspedTime'][j][c]), 16))
            #convert hex to decimal
            if len(df['ElaspedTime'][j][c]) < 2:                                        #1digit
                df['ElaspedTime'][j][c] = df['ElaspedTime'][j][c].zfill(2)              #add 0
        df['ElaspedTime'][j] = int("".join(df['ElaspedTime'][j]))

print("Data Convert:\n ChargeCurrent, ChargeVoltage, AccumulatedWatt, AccessId, ElaspedTime")
data_convert(csr_original, csr_parsing)

csr_parsing['Send'] = csr_mt['Send'].copy()
csr_parsing['msgId'] = csr_mt['msgId'].copy()
csr_parsing.insert(0, 'RegDt', csr_mt['RegDt'].copy())

save_file = "dc_100kW_csr.csv"
print("Save File: {}".format(save_file))
csr_parsing.to_csv(args.data_path + save_file, index=False)
