print("Starting...");

import csv, codecs, datetime
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import itertools

total_0 = 0;
total_1 = 0;
total_2 = 0;
total_3 = 0;
total_4 = 0;
total_5 = 0;
total_6 = 0;

plt.figure(figsize=(10,5))

df_isolament = pd.read_csv('cases-birch.csv', sep=',');
df_isolament = df_isolament = df_isolament[df_isolament['class'] < 99];

def get_week(row):
    first_date = datetime.datetime(2020, 2, 2);
    last_date = first_date + datetime.timedelta(days=7)
    date = datetime.datetime.strptime(row['DATA_CONFIRMACAO'], '%Y-%m-%d');
    #print(date);
    for i in range(0,50):
        if date >= first_date and date < last_date:
            row['Semana'] = i;
            break;
        else:
            first_date += datetime.timedelta(days=7);
            last_date += datetime.timedelta(days=7);
    return row;

def get_acumulative(row):
    global total_0;
    global total_1;
    global total_2;
    global total_3;
    global total_4;
    global total_5;
    global total_6;

    if row['class'] == 0 :
        total_0 = total_0 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_0;
    elif row['class'] == 1:
        total_1 = total_1 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_1
    elif row['class'] == 2:
        total_2 = total_2 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_2;
    elif row['class'] == 3:
        total_3 = total_3 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_3;
    elif row['class'] == 4:
        total_4 = total_4 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_4;
    elif row['class'] == 5:
        total_5 = total_5 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_5;
    elif row['class'] == 6:
        total_6 = total_6 + row['cases_by_100t_people'];
        row['Quantidade de Casos'] = total_6;
    #print(row);
    return row;


df_isolament = df_isolament.apply(lambda row : get_week(row), axis = 1);
df_isolament = df_isolament.drop(['DATA_CONFIRMACAO'], axis=1);
df_isolament = df_isolament.groupby(['Semana', 'class']).agg({'cases_by_100t_people':'mean'}).reset_index();
df_isolament = df_isolament.apply(lambda row : get_acumulative(row), axis = 1);

mks = itertools.cycle(['o', 'x', '^', '+', '*', '8', 's', 'p', 'D', 'V']);
markers = [next(mks) for i in df_isolament["class"].unique()];

chart = sns.lineplot(x="Semana", y="Quantidade de Casos", hue="class", data=df_isolament, palette=["C0", "C1", "C2","C3","C4","C5", "C6"]);
#plt.setp(chart.get_xticklabels(), rotation=90);

plt.savefig('acumulative_cases_birch.png');
plt.show();

#print(df_isolament);