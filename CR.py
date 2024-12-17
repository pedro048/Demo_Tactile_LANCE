import matplotlib.pyplot as plt

# Definindo os tempos (em segundos) e os valores de frequência correspondentes (Hz)
tempos = [0, 12, 16]  # Momentos de mudança na frequência
frequencia = [0, 4, 4]  # Frequência correspondente a cada intervalo de tempo

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.step(tempos, frequencia, where='post', color='brown', linewidth=2, label="Frequência")

# Título e rótulos dos eixos
plt.title("Perfil de Frequência ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Frequência (Hz)")

# Limites dos eixos
plt.ylim(-1, 6)

# Adicionando rótulos de valores no gráfico
for i in range(len(frequencia) - 1):
    if frequencia[i] > 0:  # Exibir apenas valores diferentes de zero
        plt.text(tempos[i] + 1, frequencia[i] + 0.2, f"{frequencia[i]} Hz", color="black", ha="center")

# Adicionando grade e cor de fundo
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.gca().set_facecolor("lightgrey")

# Exibindo legenda
plt.legend(loc="upper right", fontsize=10)

# Exibindo o gráfico
plt.show()