print("Starting...");

import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import graphviz  as gp
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree, export_graphviz
from sklearn.model_selection import train_test_split


df = pd.read_csv('cnae_dataset.csv');
df['classe'] = df['classe'].astype(str);

X_train, X_test, y_train, y_test = train_test_split(df.drop(['classe', 'sum', 'Município'], axis=1), df['classe'], test_size=0.1, random_state=42);

decisionTree = DecisionTreeClassifier();
decisionTree.fit(X_train, y_train);
print(decisionTree.score(X_test, y_test));

dot_data = export_graphviz(decisionTree, out_file=None, feature_names=df.drop(['classe', 'sum', 'Município'], axis=1).columns, filled=True, rounded=True, special_characters=True, class_names=df.classe);
graph = gp.Source(dot_data);
graph.render("classe");