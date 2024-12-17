import matplotlib.pyplot as plt

# Definindo os tempos (em segundos) e os valores de duty cycle correspondentes (%)
tempos = [0, 2, 4, 6, 8, 10, 16]  # Momentos de mudança no duty cycle
duty_cycle = [23, 17, 0, 19, 24, 0, 0]  # Duty cycle correspondente a cada intervalo de tempo

# Criando o gráfico
plt.figure(figsize=(10, 6))
plt.step(tempos, duty_cycle, where='post', color='brown', linewidth=2, label="Duty Cycle")

# Título e rótulos dos eixos
plt.title("Perfil de Duty Cycle ao Longo do Tempo")
plt.xlabel("Tempo (s)")
plt.ylabel("Duty Cycle (%)")

# Limites dos eixos
plt.ylim(-5, 30)

# Adicionando rótulos de valores no gráfico
for i in range(len(duty_cycle) - 1):
    plt.text(tempos[i] + 0.5, duty_cycle[i] + 1, f"{duty_cycle[i]}%", color="black", ha="center")

# Adicionando grade e cor de fundo
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
plt.gca().set_facecolor("lightgrey")

# Exibindo legenda
plt.legend(loc="upper right", fontsize=10)

# Exibindo o gráfico
plt.show()