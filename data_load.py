import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

dc_charger = pd.read_csv("data/dc_100kW.csv")
# dc_charger = pd.read_csv("data/dc_charger_mt_16.csv")

dc_charger['msg'] = dc_charger['msg'].str.replace(' ','')

msg_type = {'05':['Access Request','충전기<-서버'], '09':['Cancel Request','충전기<-서버'], '0D':['FW Upgrade Request','충전기<-서버','v1.0'],
            '0E':['FW Upgrade Response','충전기->서버','v1.0'], '0F':['Charger Reboot Request','충전기<-서버', 'v1.0'],
            '10':['Charger Reboot Response','충전기->서버','v1.0'], '15':['Device Status Report','충전기->서버'],
            '16':['Charging Status Report','충전기->서버'], '1A':['Device Status Report ACK','충전기<-서버'],
            '1B':['Charging Status Report ACK','충전기<-서버'], '22':['Device Init Request','충전기->서버'],
            '23':['Device Init Response','충전기<-서버'], '24':['RF Card Device Status Report','충전기->서버','v0.2'],
            '25':['RF Card Status Report ACK / IC Card Payment Response','충전기<-서버','v0.2'],
            '26':['IC Card Payment Response','충전기->서버','v0.5'], '27':['RF Card Auth Cancel Report','충전기->서버','v0.5'],
            '28':['RF/IC Card Auth Cancel Response','충전기<-서버','v0.5'], '29':['IC Card Auth Cancel Report','충전기->서버','v0.6']
            }

msg_length = {'ServerId':1,'ChargerId':6,'Length':2,'MessageType':1,'SequenceNumber':1,'DataLength':1}
msg_index = {'ServerId':2,'ChargerId':14,'Length':18,'MessageType':20,'SequenceNumber':22,'DataLength':24}

csr_data = {'ChargeCurrent':'02','ChargeVoltage':'03','Temperature':'04','AccumulatedWatt':'05','AccessId':'09','ElaspedTime':'0A','ChargerNumber':'33'}
csr_index = {'ChargeCurrent':24,'ChargeVoltage':30,'Temperature':36,'AccumulatedWatt':40,'AccessId':48,'ElaspedTime':58,'ChargerNumber':66}


# save Message Type
def select_mt(df, mt):
    csr_index1 = []
    for i in range(len(df)):
        if df['msg'][i][18:20]==mt:
            csr_index1.append(i)
    df1 = df.loc[csr_index1]
    df1.to_csv("data/dc_charger_mt_{}.csv".format(mt), index=False)
    return df1

ss = select_mt(dc_charger, '16')
# ServerId, ChargerId, Length, MessageType, SequenceNumber, DataLength = [], [], [], [], [], []
# ChargeCurrent, ChargeVoltage, Temperature, AccumulatedWatt, AccessId, ElaspedTime, ChargerNumber = [], [], [], [], [], [], []
#
# for index in dc_charger.index:
#     ServerId.append(dc_charger['msg'][index][:msg_index['ServerId']])
#     ChargerId.append(dc_charger['msg'][index][msg_index['ServerId']:msg_index['ChargerId']])
#     Length.append(dc_charger['msg'][index][msg_index['ChargerId']:msg_index['Length']])
#     MessageType.append(dc_charger['msg'][index][msg_index['Length']:msg_index['MessageType']])
#     SequenceNumber.append(dc_charger['msg'][index][msg_index['MessageType']:msg_index['SequenceNumber']])
#     DataLength.append(dc_charger['msg'][index][msg_index['SequenceNumber']:msg_index['DataLength']])
#
#     #Charging Status Report
#     ChargeCurrent.append(dc_charger['msg'][index][csr_index['ChargeCurrent']+2:csr_index['ChargeVoltage']])   #0x02 value:2
#     ChargeVoltage.append(dc_charger['msg'][index][csr_index['ChargeVoltage']+2:csr_index['Temperature']])     #0x03 value:2
#     Temperature.append(dc_charger['msg'][index][csr_index['Temperature']+2:csr_index['AccumulatedWatt']])     #0x04 value:2
#     AccumulatedWatt.append(dc_charger['msg'][index][csr_index['AccumulatedWatt']+2:csr_index['AccessId']])    #0x05 value:3
#     AccessId.append(dc_charger['msg'][index][csr_index['AccessId']+2:csr_index['ElaspedTime']])               #0x09 value:4
#     ElaspedTime.append(dc_charger['msg'][index][csr_index['ElaspedTime']+2:csr_index['ChargerNumber']])       #0x0A value:3
#     ChargerNumber.append(dc_charger['msg'][index][csr_index['ChargerNumber']+2:-2])                           #0x33 value:2
#
#
# csr = pd.DataFrame({'ServerId':ServerId, 'ChargerId':ChargerId, 'Length':Length, 'MessageType':MessageType,
#                     'SequenceNumber':SequenceNumber, 'DataLength':DataLength, 'ChargeCurrent':ChargeCurrent,
#                     'ChargeVoltage':ChargeVoltage, 'Temperature':Temperature, 'AccumulatedWatt':AccumulatedWatt,
#                     'AccessId':AccessId, 'ElaspedTime':ElaspedTime, 'ChargerNumber':ChargerNumber
#                     })
#
# # csr['RegDt', 'Send','msgId'] = dc_charger[['RegDt', 'Send','msgId']].copy()
# csr['RegDt'] = dc_charger[['RegDt']].copy()
# csr['Send'] = dc_charger[['Send']].copy()
# csr['msgId'] = dc_charger[['msgId']].copy()
#
#
# csr.ServerId.value_counts()
# csr.ServerId.nunique()
#
#
#
# #change unit
# for k in range(len(csr)):
#     csr['ChargeCurrent'][k] = (int((csr['ChargeCurrent'][k]), 16)) *10 / 1000       #10mA
#     csr['ChargeVoltage'][k] = (int((csr['ChargeVoltage'][k]), 16)) *100 / 1000      #100mV
#     csr['AccumulatedWatt'][k] = (int((csr['AccumulatedWatt'][k]), 16)) *100 / 1000  #1000mWh




# plt.plot(csr_aw)
# plt.show()

