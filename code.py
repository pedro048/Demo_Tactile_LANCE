import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from scipy.cluster.hierarchy import dendrogram, linkage

# Criar o dataset de exemplo
X, y = make_blobs(random_state=1)

# Realizar o linkage para criar a hierarquia dos clusters
Z = linkage(X, method='ward')

# Plotar o dendrograma
plt.figure(figsize=(10, 5))
dendrogram(Z)
plt.title('Dendrograma do Agrupamento Hierárquico')
plt.xlabel('Índices das amostras')
plt.ylabel('Distância')
plt.show()