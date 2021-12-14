import pandas as pd
import os
import argparse
import statistics as stat           # statistics  module
from common import Data             # common  module
import chart                        # chart  module

pd.set_option('mode.chained_assignment', None)

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file = Data()
print("File List: {}".format(file.file_name))

#충전기 선택
select_file = file.file_name[0]
print("Select File: {}".format(select_file))
file_path = args.data_path + select_file + ".csv"

original_file = pd.read_csv(file_path)
original_file = stat.convert_datetime(original_file)

msg_sequence = stat.sequence_mt(original_file)
msg_sequence['mt'].unique()
msg_sequence['exp'].value_counts()
msg_sequence['exp'].value_counts().sum()

chart.show_value_cnt(msg_sequence, "msg type", 'exp')