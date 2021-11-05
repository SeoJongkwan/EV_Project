import pandas as pd

class Data:
    base_index = []
    type = {}

    def __init__(self):
        self.file_name = ["dc_100kW_인덕원IT밸리","dc_50kW_광주보건환경연구원","dc_50kW_국민차매매단지공항점","dc_50kW_해오름휴게소","dc_50kW_현대이엔지세종사옥"]

    def read_file(self, name):
        file = pd.read_csv(name)
        file['msg'] = file['msg'].str.replace(' ', '')
        return file

    # structure: name[length:data]
    def structure(self):
        header = {'ServerId':[1, '0x00'], 'ChargerId':[6,'0xXX'], 'Length':[2,'0xXX']}
        body = {'MessageType':[1,'0xXX'],'SequenceNumber':[1,'0xXX'], 'DataLength':[1,'0xXX'],'Data':['n','0xXX']}
        #data location
        serverId_index = header["ServerId"][0]*2
        ChargerId_index = serverId_index+(header['ChargerId'][0]*2)
        Length_index = ChargerId_index+(header['Length'][0]*2)

        mt_index = Length_index+(body['MessageType'][0]*2)
        seq_index = mt_index+(body['SequenceNumber'][0]*2)
        dl_index = seq_index+(body['DataLength'][0]*2)

        Data.base_index.extend([serverId_index, ChargerId_index, Length_index, mt_index, seq_index, dl_index])
        return Data.base_index

    def msg_type(self):
        mt = {'05':['Access Request','충전기<-서버'], '09':['Cancel Request','충전기<-서버'], '0D':['FW Upgrade Request','충전기<-서버','v1.0'],
                '0E':['FW Upgrade Response','충전기->서버','v1.0'], '0F':['Charger Reboot Request','충전기<-서버', 'v1.0'],
                '10':['Charger Reboot Response','충전기->서버','v1.0'], '15':['Device Status Report','충전기->서버'],
                '16':['Charging Status Report','충전기->서버'], '1A':['Device Status Report ACK','충전기<-서버'],
                '1B':['Charging Status Report ACK','충전기<-서버'], '22':['Device Init Request','충전기->서버'],
                '23':['Device Init Response','충전기<-서버'], '24':['RF Card Device Status Report','충전기->서버','v0.2'],
                '25':['RF Card Status Report ACK / IC Card Payment Response','충전기<-서버','v0.2'],
                '26':['IC Card Payment Response','충전기->서버','v0.5'], '27':['RF Card Auth Cancel Report','충전기->서버','v0.5'],
                '28':['RF/IC Card Auth Cancel Response','충전기<-서버','v0.5'], '29':['IC Card Auth Cancel Report','충전기->서버','v0.6']
                }
        return mt

    def select_mt(self, data, mt):
        self.data = data
        self.mt = mt
        index = []
        for i in range(len(self.data)):
            if self.data['msg'][i][Data.base_index[2]:Data.base_index[3]] == mt:
                index.append(i)
        self.data = self.data.loc[index].reset_index(drop=True)
        Data.type = Data.msg_type(self)
        print("Message Type: {} {}".format(self.mt, Data.type[self.mt]))
        return self.data




