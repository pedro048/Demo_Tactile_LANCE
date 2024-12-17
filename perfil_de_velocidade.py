import matplotlib.pyplot as plt
import numpy as np

# Usando o estilo 'ggplot' para uma visualização mais científica
plt.style.use('ggplot')

# Velocidades em px/s para cada segmento
velocidades = [93, 24, 96, 46, 106, 53, 33, 35]

# Tempo em segundos para cada velocidade (2 segundos cada)
tempo_por_segmento = 2
tempos = np.arange(0, tempo_por_segmento * len(velocidades), tempo_por_segmento)

# Gerando os valores de tempo e velocidade para o gráfico
tempo = []
velocidade = []

for i, v in enumerate(velocidades):
    tempo.extend([tempos[i], tempos[i] + tempo_por_segmento])
    velocidade.extend([v, v])

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.step(tempo, velocidade, where='post', color='brown', linewidth=2, label="Perfil de Velocidade")

# Título e rótulos dos eixos
plt.title("Perfil de Velocidade ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Velocidade (px/s)")

# Limites dos eixos
plt.ylim(20, 120)

# Adicionando rótulos de valores no gráfico
for i in range(len(velocidades)):
    plt.text(tempos[i] + 1, velocidades[i] + 2, f"{velocidades[i]} px/s", color="black", ha="center")

# Adicionando grade e cor de fundo
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.gca().set_facecolor("lightgrey")

# Exibindo legenda
plt.legend(loc="upper right", fontsize=10)

# Exibindo o gráfico
plt.show()