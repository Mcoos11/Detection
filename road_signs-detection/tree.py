import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import csv

def gen_tree():
    color = []
    shape = []
    target = []

    ##wczytywanie danych uczących
    #kolor: 0-360
    #ksztalt: 11-kolo, 12-kwadrat, 13-trojkat
    #odp: 1-ostrzegawczy, 2-nakazu, 3-zakazu, 4-informacyjny
    with open('data.csv', 'r', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile, delimiter=';')
        for row in csvreader:
            color.append(int(row['color']))
            shape.append(int(row['shape']))
            target.append(int(row['type']))
        csvfile.close()

    ##przygotowanie danych uczących i ich statystyki
    data = np.c_[color, shape, target]
    df_data = pd.DataFrame(data, columns=['color', 'shape', 'label'])
    print("Dane uczace")
    print(df_data.head())
    print("\ninformacje ststystyczne")
    print(df_data.describe().apply(lambda x: round(x, 2)))
    print("\nrozlorzenie typow")
    print(df_data.label.value_counts())

    ##drzewo
    tree = DecisionTreeClassifier(criterion="gini", max_depth=4, random_state=2)
    X = np.c_[color, shape]
    Y = np.array(target)
    tree.fit(X, Y)
    print("\nDokladnosc drzewa")
    print(tree.score(X, Y))

    return tree, X, Y