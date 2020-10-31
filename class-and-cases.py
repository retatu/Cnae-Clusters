print("Starting...");

import csv, codecs, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df_class = pd.read_csv('cnae_dataset_kmeans.csv', sep=',');
df_class = df_class.filter(['Município', 'classe']);
df_covid = pd.read_csv('covid-rs.csv', sep=';', encoding='UTF-8');
df_population = pd.read_csv('population.csv', sep=',');

df_covid['DATA_CONFIRMACAO'] =  pd.to_datetime(df_covid['DATA_CONFIRMACAO']);
df_covid = df_covid.filter(['DATA_CONFIRMACAO', 'MUNICIPIO']);
df_covid = df_covid.groupby(['DATA_CONFIRMACAO', 'MUNICIPIO']).size().reset_index(name='cases');

def get_class(row):
    try:
        value = df_class.loc[df_class['Município'].str.lower() == row['MUNICIPIO'].lower(), 'classe'];
        row['class'] = value.values[0];
    except:
        row['class'] = 99;
        print(row['MUNICIPIO']);
    return row;

def get_week(row):
    first_date = datetime.datetime(2020, 2, 2);
    last_date = first_date + datetime.timedelta(days=7)
    date = row['DATA_CONFIRMACAO'];
    #print(date);
    for i in range(0,50):
        if date >= first_date and date < last_date:
            row['week'] = i;
            break;
        else:
            first_date += datetime.timedelta(days=7);
            last_date += datetime.timedelta(days=7);
    return row;

def get_total_population(row):
    value = df_population.loc[df_population['cidade'].str.lower() == row['MUNICIPIO'].lower(), 'populacao'];
    try:
        row['population'] = value.values[0];
    except:
        print(row['MUNICIPIO']);
    return row;

def get_cases_by_100t_people(row):
    try:
        row['cases_by_100t_people'] = (100000 * row['cases'])/row['population'];
    except:
        print(row['cases']);
        print(row['population']);
    return row;


df_covid = df_covid.apply(lambda row: get_class(row), axis=1);
df_covid = df_covid.apply(lambda row: get_week(row), axis = 1);
df_covid = df_covid.apply(lambda row: get_total_population(row), axis=1);
df_covid = df_covid.apply(lambda row: get_cases_by_100t_people(row), axis=1);


df_covid = df_covid.drop(['MUNICIPIO', 'cases'], axis=1);

df_covid = df_covid.groupby(['DATA_CONFIRMACAO', 'class']).agg({'cases_by_100t_people':'mean'}).reset_index();

df_covid.to_csv('cases-kmeans.csv');








