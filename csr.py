import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import data_load


csr_data = {'ChargeCurrent': '02', 'ChargeVoltage': '03', 'Temperature': '04', 'AccumulatedWatt': '05',
            'AccessId': '09', 'ElaspedTime': '0A', 'ChargerNumber': '33'}
csr_index = {'ChargeCurrent': 24, 'ChargeVoltage': 30, 'Temperature': 36, 'AccumulatedWatt': 40, 'AccessId': 48,
             'ElaspedTime': 58, 'ChargerNumber': 66}


# save Message Type CSV file --> view msg_type
def select_mt(df, mt):
    csr_index1 = []
    for i in range(len(df)):
        if df['msg'][i][18:20] == mt:
            csr_index1.append(i)
    df1 = df.loc[csr_index1]
    df1.to_csv("data/dc_charger_mt_{}.csv".format(mt), index=False)
    return df1


csr_mt = select_mt(dc_charger, '16').reset_index(drop=True)
ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
ChargeCurrent, ChargeVoltage, Temperature, AccumulatedWatt, AccessId, ElaspedTime, ChargerNumber = [], [], [], [], [], [], []

# data parsing: msg_length * 2 = actual msg length
for index in csr_mt.index:
    ServerId.append(csr_mt['msg'][index][:msg_index['ServerId']])
    ChargerId.append(csr_mt['msg'][index][msg_index['ServerId']:msg_index['ChargerId']])
    Length.append(csr_mt['msg'][index][msg_index['ChargerId']:msg_index['Length']])
    MessageType.append(csr_mt['msg'][index][msg_index['Length']:msg_index['MessageType']])
    SequenceNumber.append(csr_mt['msg'][index][msg_index['MessageType']:msg_index['SequenceNumber']])
    DataLength.append(csr_mt['msg'][index][msg_index['SequenceNumber']:msg_index['DataLength']])

    # Charging Status Report
    ChargeCurrent.append(
        csr_mt['msg'][index][csr_index['ChargeCurrent'] + 2:csr_index['ChargeVoltage']])  # 0x02 value:2
    ChargeVoltage.append(csr_mt['msg'][index][csr_index['ChargeVoltage'] + 2:csr_index['Temperature']])  # 0x03 value:2
    Temperature.append(csr_mt['msg'][index][csr_index['Temperature'] + 2:csr_index['AccumulatedWatt']])  # 0x04 value:2
    AccumulatedWatt.append(csr_mt['msg'][index][csr_index['AccumulatedWatt'] + 2:csr_index['AccessId']])  # 0x05 value:3
    AccessId.append(csr_mt['msg'][index][csr_index['AccessId'] + 2:csr_index['ElaspedTime']])  # 0x09 value:4
    ElaspedTime.append(csr_mt['msg'][index][csr_index['ElaspedTime'] + 2:csr_index['ChargerNumber']])  # 0x0A value:3
    ChargerNumber.append(csr_mt['msg'][index][csr_index['ChargerNumber'] + 2:-2])  # 0x33 value:2

csr_original = pd.DataFrame({'ServerId': ServerId, 'ChargerId': ChargerId, 'Length': Length, 'MessageType': MessageType,
                             'SequenceNumber': SequenceNumber, 'DataLength': DataLength, 'ChargeCurrent': ChargeCurrent,
                             'ChargeVoltage': ChargeVoltage, 'Temperature': Temperature,
                             'AccumulatedWatt': AccumulatedWatt,
                             'AccessId': AccessId, 'ElaspedTime': ElaspedTime, 'ChargerNumber': ChargerNumber
                             })

csr = csr_original.copy()
csr['RegDt'] = dc_charger['RegDt'].copy()
csr['Send'] = dc_charger['Send'].copy()
csr['msgId'] = dc_charger['msgId'].copy()

# change unit
for k in range(len(csr)):
    csr['ChargeCurrent'][k] = (int((csr['ChargeCurrent'][k]), 16)) * 10 / 1000  # 10mA
    csr['ChargeVoltage'][k] = (int((csr['ChargeVoltage'][k]), 16)) * 100 / 1000  # 100mV
    csr['AccumulatedWatt'][k] = (int((csr['AccumulatedWatt'][k]), 16)) * 100 / 1000  # 1000mWh

# ElaspedTime: HH:MM:SS
for j in range(len(csr)):
    csr['ElaspedTime'][j] = [csr['ElaspedTime'][j][i:i + 2] for i in range(0, len(csr['ElaspedTime'][j]), 2)]
    for k in range(len(csr['ElaspedTime'][j])):
        csr['ElaspedTime'][j][k] = str(int((csr['ElaspedTime'][j][k]), 16))  # convert hex to decimal
        if len(csr['ElaspedTime'][j][k]) < 2:  # 1digit
            csr['ElaspedTime'][j][k] = csr['ElaspedTime'][j][k].zfill(2)  # add 0
    csr['ElaspedTime'][j] = ''.join(csr['ElaspedTime'][j])  # join list element

csr["RegDt"] = pd.to_datetime(csr["RegDt"], format='%Y-%m-%d %H:%M:%S')
cols = ["ChargeCurrent", "ChargeVoltage", "Temperature", "AccumulatedWatt"]
csr[cols] = csr[cols].apply(pd.to_numeric)

# csr.columns
# csr.dtypes
# csr.describe()

csr.ServerId.value_counts()
csr.ServerId.nunique()

col = ['RegDt', 'ElaspedTime', 'ChargerId', 'SequenceNumber', 'AccumulatedWatt', 'ChargeCurrent', 'ChargeVoltage',
       'Send']
csr_col = csr[col]
csr_scv = csr_col[csr_col['Send'] == 'S']
csr_rcv = csr_col[csr_col['Send'] == 'R']

# plt.plot(csr["RegDt"], csr["AccumulatedWatt"])
# sns.distplot(csr["AccumulatedWatt"])
# plt.show()