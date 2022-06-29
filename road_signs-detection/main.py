import pyimagesearch.learning_data as id
import pyimagesearch.predict as pd
import tree
import matplotlib.pyplot as plt
from mlxtend.plotting import plot_decision_regions
from sklearn.tree import export_graphviz

while(True):
    print("MENU")
    print("1 - uczenie\n2 - rozpoznawanie\n3 - pokaz wykres\n4 - stworz graf\n5 - wyjscie")
    choice = input()

    if(choice == '1'):
        id.gen_data()
        Tree, X, Y = tree.gen_tree()
    elif(choice == '2'):
        name = input("wprowadz nazwe pliku\n")
        pd.prediction(Tree, str(name))
    elif (choice == '3'):
        plt.figure(2)
        ax = plot_decision_regions(X, Y, Tree, colors = 'blue,orange,green,red')
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles,['ostrzegawczy', 'nakazu', 'zakazu', 'informacyjny'], framealpha=0.3)
        plt.xlabel("Kolor")
        plt.ylabel("Ksztalt")
        plt.show()
    elif(choice == '4'):
        export_graphviz(Tree, out_file='graph.dot', feature_names=['kolor', 'ksztalt'], class_names=['ostrzegawczy', 'nakazu', 'zakazu', 'informacyjny'], rounded=True, filled=True)
    elif (choice == '5'):
        break
    else:
        print("Nie ma takiej opcji\n")

