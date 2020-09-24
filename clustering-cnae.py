print("Starting...");

import csv, codecs, datetime
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import sklearn.cluster as lib_cluster
from ftfy import fix_encoding
from sklearn.preprocessing import MinMaxScaler
from sklearn.ensemble import RandomForestClassifier

dfs = list();


def get_percentagens(row):
    row['agropecuario'] = row['agropecuario']/row['sum']*100
    row['transformacao/industrial'] = row['transformacao/industrial']/row['sum']*100
    row['comercio e atividades essenciais'] = row['comercio e atividades essenciais']/row['sum']*100
    row['atividades financeiras servicos profissionais e tecnicos'] = row['atividades financeiras servicos profissionais e tecnicos']/row['sum']*100
    row['administracao publica'] = row['administracao publica']/row['sum']*100
    row['saude'] = row['saude']/row['sum']*100
    row['educacao e cultura'] = row['educacao e cultura']/row['sum']*100
    return row

for i in range (1, 22):
    df = pd.read_csv('datasets-cnae/'+str(i)+'.csv', encoding='ISO-8859-1', sep=';', skiprows=5, thousands='.');
    df = df.drop(axis=1, columns = ['ibge', 'latitude', 'longitude'])
    df.columns = ['Município', str(i)]
    dfs.append(df)

#Now I need to sum the values which are in these positions: (1,2), (3,4,5,6), (7,8,9,10), (11,12,13,14,19,20), (15), (17), (16,18,21)
df = pd.DataFrame()
df = pd.concat(dfs, axis=1)
#df = df.groupby([df['Município']]).agg({'2018 (-)': 'sum'}).reset_index()
df = df.loc[:,~df.columns.duplicated()]
print(df)
df['agropecuario'] = df.loc[:,['1', '2']].sum(axis=1)
df['transformacao/industrial'] = df.loc[:,['3', '4', '5', '6']].sum(axis=1)
df['comercio e atividades essenciais'] = df.loc[:,['7','8','9','10']].sum(axis=1)
df['atividades financeiras servicos profissionais e tecnicos'] = df.loc[:,['11', '12', '13', '14', '19', '20']].sum(axis=1)
df['administracao publica'] = df.loc[:,['15']].sum(axis=1)
df['saude'] = df.loc[:,['17']].sum(axis=1)
df['educacao e cultura'] = df.loc[:,['16', '18', '21']].sum(axis=1)
df = df.drop(axis=1, columns = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21'])
sum_column = df['agropecuario'] + df['transformacao/industrial'] + df['comercio e atividades essenciais'] + df['atividades financeiras servicos profissionais e tecnicos'] + df['administracao publica'] + df['saude'] + df['educacao e cultura']
df["sum"] = sum_column
#change to percentagens:
df = df.apply(lambda row: get_percentagens(row), axis=1)

cluster = lib_cluster.Birch(n_clusters=7).fit(df.drop(axis=1, columns = ['Município', 'sum']))
print(cluster.labels_)
df['classe'] = cluster.labels_
df.to_csv('cnae_dataset.csv', index=False);