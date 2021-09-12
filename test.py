import pandas as pd
import os
import argparse
import psycopg2
import configparser
import csv

conf = configparser.ConfigParser()
conf.read('info.init')

dbname = conf.get('DB', 'dbname')
host = conf.get('DB', 'host')
user = conf.get('DB', 'user')
password = conf.get('DB', 'password')
port = conf.get('DB', 'port')

print("<DB Info>")
print("name:", dbname + "\nhost:", host + "\nport:", port)

con = psycopg2.connect(host=host, dbname=dbname, user=user, password=password, port=port)
cursor = con.cursor()

path = os.path.join(os.path.dirname(__file__), 'data/')
parser = argparse.ArgumentParser()
parser.add_argument('--data_path', default=path, help = "path to input file")
args = parser.parse_args()

file_name = "dc_100kW_csr.csv"
data = pd.read_csv(args.data_path + file_name, dtype='str')
PATH = args.data_path + file_name

data.columns
data.insert(0, 'test', 4)

