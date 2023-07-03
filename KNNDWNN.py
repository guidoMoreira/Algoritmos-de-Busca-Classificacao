#VERSÂO FINAL AQUI
import numpy as np
import random
import scipy.stats as ss
import matplotlib.pyplot as plt

#Calcula distância entre dois pontos
def distance(p1, p2):
    return np.sqrt(np.sum(np.power(p2-p1, 2)))

#Retorna a classe prevista baseado nos votos dos k vizinhos mais proximos
def MaisVotos(votes):
    vote_counts = {}
    for vote in votes:
        if vote in vote_counts:
           vote_counts[vote]+= 1
        else:
            vote_counts[vote]= 1
    winners = []
    max_count = max(vote_counts.values())
    for vote, count in vote_counts.items():
        if count == max_count:
            winners.append(vote)
    return random.choice(winners)

def encontraMaisProxim(p, points, k = 5):
    distances = np.zeros(points.shape[0])
    for i in range(len(distances)):
        distances[i]= distance(p, points[i])
    ind = np.argsort(distances)
    return ind[:k]

def distWeight(p,points):
    Dist = np.zeros(points.shape[0])
    for i in range(len(Dist)):
        Dist[i]= distance(p, points[i])
        
    sum = 0
    InvDist = np.zeros(points.shape[0])
    for i in range(len(Dist)):
      if Dist[i]>0:
        InvDist[i] = 1.0/Dist[i]
      else:
        InvDist[i] = 1.0
      sum+=InvDist[i]
    InvDist/=sum
    return InvDist

#previsão
def knn_predict(p, points, outcomes, k = 5):
    ind = encontraMaisProxim(p, points, k)
    return MaisVotos(outcomes[ind])

def dwnn_predict(p, points, outcomes):
    Ivd = distWeight(p, points)
    classes = []
    votes = []
    countVoters = []
    for i in range(len(Ivd)):
      if outcomes[i] not in classes:
        classes.append(outcomes[i])
        votes.append(0)
        countVoters.append(0)
      indiceC = classes.index(outcomes[i])
      votes[indiceC] += Ivd[i]
      countVoters[indiceC]+=1
    for i in range(len(votes)):
      votes[i]/=countVoters[i]
    return votes.index(max(votes))


'''Visualização Top
def make_prediction_grid(predictors, outcomes, limits, h, k):
    (x_min, x_max, y_min, y_max) = limits
    xs = np.arange(x_min, x_max, h)
    ys = np.arange(y_min, y_max, h)
    xx, yy = np.meshgrid(xs, ys)

    prediction_grid = np.zeros(xx.shape, dtype = int)
    for i, x in enumerate(xs):
        for j, y in enumerate(ys):
            p = np.array([x, y])
            prediction_grid[j, i] = knn_predict(p, predictors, outcomes, k)
    return (xx, yy, prediction_grid)

def plot_prediction_grid (xx, yy, prediction_grid, filename):
    """ Plot KNN predictions for every point on the grid."""
    from matplotlib.colors import ListedColormap
    background_colormap = ListedColormap (["hotpink", "lightskyblue", "yellowgreen"])
    observation_colormap = ListedColormap (["red", "blue", "green"])
    plt.figure(figsize =(10, 10))
    plt.pcolormesh(xx, yy, prediction_grid, cmap = background_colormap, alpha = 0.5)
    plt.scatter(predictors[:, 0], predictors [:, 1], c = outcomes, cmap = observation_colormap, s = 50)
    plt.xlabel('Variable 1'); plt.ylabel('Variable 2')
    plt.xticks(()); plt.yticks(())
    plt.xlim (np.min(xx), np.max(xx))
    plt.ylim (np.min(yy), np.max(yy))
    plt.savefig(filename)
'''
'''
iris = datasets.load_iris()
    # >>>iris["data"]
predictors = iris.data[:, 0:4]
outcomes = iris.target
'''


import openml
from openml.datasets import edit_dataset, fork_dataset, get_dataset

dataset = openml.datasets.get_dataset(1063)

predictors = dataset.get_data(dataset_format="array",target=dataset.default_target_attribute)[0]

outcomes = dataset.get_data(dataset_format="array",target=dataset.default_target_attribute)[1]


'''
plt.plot(predictors[outcomes == 0][:, 0], predictors[outcomes == 0][:, 1], "ro")
plt.plot(predictors[outcomes == 1][:, 0], predictors[outcomes == 1][:, 1], "go")
plt.plot(predictors[outcomes == 2][:, 0], predictors[outcomes == 2][:, 1], "bo")

k = 5; filename ="iris_grid.pdf"; limits =(4, 8, 1.5, 4.5); h = 0.1
#(xx, yy, prediction_grid) = make_prediction_grid(predictors, outcomes, limits, h, k)
plot_prediction_grid(xx, yy, prediction_grid, filename)
#plt.show()
'''


#knn feito
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

#Usar parcela para prever restante
X_train, X_test, y_train, y_test = train_test_split(predictors, outcomes, test_size=0.8, random_state=3)

#Usar tudo para prever
#X_train = predictors
#y_train = outcomes

#Testar previsão em tudo
X_test = X_train
y_test = y_train


knn = KNeighborsClassifier(n_neighbors = 3)#weights='distance')
dwnn = KNeighborsClassifier(weights='distance')
knn.fit(X_train, y_train)
dwnn.fit(X_train, y_train)
sk_predictions = knn.predict(X_test)
sk_predictionsD = dwnn.predict(X_test)

#knn manual
my_predictions = np.array([knn_predict(p, X_train, y_train, 3) for p in X_test])

my_predictionsD = np.array([dwnn_predict(p, X_train, y_train) for p in X_test])


print("previsão scikitLearn: ")
print(100 * np.mean(sk_predictions == y_test))
print("previsão nossa: ")
print(100 * np.mean(my_predictions == y_test))

print("previsão scikitLearn: ")
print(100 * np.mean(sk_predictionsD == y_test))
print("previsão nossa: : ")
print(100 * np.mean(my_predictionsD == y_test))