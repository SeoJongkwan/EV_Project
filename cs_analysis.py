import pandas as pd
import argparse
import os

from common import Data             #common module
import statistics as stat           #statistics  module
import chart                        #chart  module


path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()
select_file = file.file_name[1]
print("Select File: {}".format(select_file))

original_file = pd.read_csv(args.data_path + select_file + ".csv")

csr_file = pd.read_csv(args.data_path + select_file + "_csr.csv")
csr_ack_file = pd.read_csv(args.data_path + select_file + "_csr_ack.csv")
csr_file = stat.convert_datetime(csr_file)
csr_ack_file = stat.convert_datetime(csr_ack_file)

csr_cols = ['RegDt','ChargerId','ChargeCurrent','ChargeVoltage','AccumulatedWatt','ChargerNumber']
csr = csr_file[csr_cols]
csr = csr.copy()
csr['RegDt'] = pd.to_datetime(csr['RegDt'], format='%Y-%m-%d %H:%M:%S')

csr_ack_cols = ['RegDt','ChargerId','RequireWatt','ChargingFee']
csr_ack = csr_ack_file[csr_ack_cols]
csr_ack = csr_ack.copy()
csr_ack['RegDt'] = pd.to_datetime(csr_ack['RegDt'], format='%Y-%m-%d %H:%M:%S')


#delete NAN data
csr = stat.check_nan_value(csr)
csr_ack = stat.check_nan_value(csr_ack)



# chart.show_density(csr, 'AccumulatedWatt')

t = csr.loc[csr['RegDt'].dt.month == 9]
# chart.show_variable_relation(t, 'RegDt', 'ChargeCurrent', 'AccumulatedWatt')

# chart.show_feature_correlation(csr, 'RegDt', 'AccumulatedWatt')


original_file = stat.convert_datetime(original_file)
msg_sequence = stat.sequence_mt(original_file)
msg_sequence['mt'].unique()
msg_sequence['exp'].value_counts().sum()

chart.show_msg_period_statistics(msg_sequence, select_file, '05')
