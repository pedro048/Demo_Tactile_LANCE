import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pyautogui
import time
from matplotlib.backends.backend_pdf import PdfPages

# Dados fornecidos
points = [(444, 813), (456, 627), (505, 627), (512, 818), (605, 815), (585, 605), (562, 501), (533, 442), (498, 503)]
speeds = [93, 24, 96, 46, 106, 53, 33, 35]  # px/s
trajet_ids = [3, 3, 2, 3, 3, 0, 1, 1]
time_per_trajet = 2  # segundos por trajeto
total_time = time_per_trajet * len(speeds)

# Configurações para as IDs
configurations = {
    0: {"freq_low": 0, "freq_high": 0, "duty_low": 0, "duty_high": 0},
    1: {"freq_low": 4, "freq_high": 7, "duty_low": 32, "duty_high": 32},
    2: {"freq_low": 12, "freq_high": 40, "duty_low": 34, "duty_high": 34},
    3: {"freq_low": 167, "freq_high": 167, "duty_low": 17, "duty_high": 24}
}

vel_min = 24  # Velocidade mínima do cursor em px/s
vel_max = 106  # Velocidade máxima do cursor em px/s

# Funções auxiliares
def limited_vel(vel, vel_min, vel_max):
    return max(min(vel, vel_max), vel_min)

def frequency(vel, vel_min, vel_max, freq_low, freq_high):
    cursor_vel = limited_vel(vel, vel_min, vel_max)
    return ((freq_high - freq_low) / (vel_max - vel_min)) * (cursor_vel - vel_min) + freq_low

def duty_cycle(vel, vel_min, vel_max, duty_low, duty_high):
    cursor_vel = limited_vel(vel, vel_min, vel_max)
    return ((duty_high - duty_low) / (vel_max - vel_min)) * (cursor_vel - vel_min) + duty_low

# Iniciar após 5 segundos
print("Iniciando em 5 segundos...")
time.sleep(5)

# Inicializando listas para os dados dos gráficos e tabela
data = []

# Inicializando listas para os dados dos gráficos
time_stamps = []
velocities = []
frequencies_id1, duty_cycles_id1 = [], []
frequencies_id2, duty_cycles_id2 = [], []
frequencies_id3, duty_cycles_id3 = [], []

current_time = 0

# Movimentar o cursor ao longo dos pontos na velocidade definida
for i in range(len(points) - 1):
    start_point = points[i]
    end_point = points[i + 1]
    final_speed = speeds[i]  # Velocidade final para o trajeto atual
    traj_id = trajet_ids[i]
    config = configurations[traj_id]
    
    # Dividindo o tempo de cada trajeto em subintervalos
    sub_intervals = 20
    interval_duration = time_per_trajet / sub_intervals
    speed_increment = final_speed / sub_intervals  # Incremento gradual de velocidade

    for j in range(sub_intervals):
        # Calcular a velocidade para o subintervalo atual
        current_speed = speed_increment * (j + 1)
        
        # Atualizar as listas para os gráficos
        time_stamps.append(current_time)
        velocities.append(current_speed)

        # Gráficos específicos para cada ID
        if traj_id == 1:
            freq = frequency(current_speed, vel_min, vel_max, config["freq_low"], config["freq_high"])
            frequencies_id1.append(freq)
            duty_cycles_id1.append(32)  # Duty cycle constante para ID 1
        else:
            frequencies_id1.append(0)
            duty_cycles_id1.append(0)

        if traj_id == 2:
            freq = frequency(current_speed, vel_min, vel_max, config["freq_low"], config["freq_high"])
            frequencies_id2.append(freq)
            duty_cycles_id2.append(34)  # Duty cycle constante para ID 2
        else:
            frequencies_id2.append(0)
            duty_cycles_id2.append(0)

        if traj_id == 3:
            duty = duty_cycle(current_speed, vel_min, vel_max, config["duty_low"], config["duty_high"])
            duty_cycles_id3.append(duty)
            frequencies_id3.append(167)  # Frequência constante para ID 3
        else:
            duty_cycles_id3.append(0)
            frequencies_id3.append(0)

        # Definir frequências e duty cycles para a tabela e gráficos
        freq, duty = 0, 0
        if traj_id == 1:
            freq = frequency(current_speed, vel_min, vel_max, config["freq_low"], config["freq_high"])
            duty = 32
        elif traj_id == 2:
            freq = frequency(current_speed, vel_min, vel_max, config["freq_low"], config["freq_high"])
            duty = 34
        elif traj_id == 3:
            freq = 167
            duty = duty_cycle(current_speed, vel_min, vel_max, config["duty_low"], config["duty_high"])

        # Adicionar dados à lista
        data.append([current_time, current_speed, freq, duty])    

        current_time += interval_duration

    # Mover o cursor ao longo do trajeto em tempo real
    pyautogui.moveTo(start_point[0], start_point[1])
    pyautogui.moveTo(end_point[0], end_point[1], duration=time_per_trajet)

# Criar DataFrame com os dados e verificar o tempo de amostragem
df = pd.DataFrame(data, columns=["Time", "Speed", "Frequency", "Duty Cycle"])
sampling_interval = df["Time"].diff().mean()
print(f"Tempo de amostragem médio: {sampling_interval:.4f} segundos")

# Salvar a tabela como CSV
df.to_csv("cursor_trajectory_data.csv", index=False)

# Função para configurar o estilo do gráfico
def apply_style():
    plt.grid(True)
    plt.gca().set_facecolor("lightgrey")
    plt.legend()
    plt.tight_layout()

# Salvar gráficos em um arquivo PDF
with PdfPages("cursor_trajectory_plots.pdf") as pdf:
    # Gráfico de Velocidade
    plt.figure()
    plt.plot(time_stamps, velocities, color='red', label=r"$c_{\text{speed}}$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$c_{\text{speed}}$ (px/s)")
    plt.title(r"$c_{\text{speed}}$ profile")
    apply_style()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Frequência e Duty Cycle para ID 1
    plt.figure()
    plt.plot(time_stamps, frequencies_id1, color='green', label=r"$f$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$f$ (Hz)")
    plt.title(r"$f$ for CR")
    apply_style()
    pdf.savefig()
    plt.close()
    
    plt.figure()
    plt.plot(time_stamps, duty_cycles_id1, color='green', label=r"$d$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$d$ (%)")
    plt.title(r"$d$ for CR")
    apply_style()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Frequência e Duty Cycle para ID 2
    plt.figure()
    plt.plot(time_stamps, frequencies_id2, color='purple', label=r"$f$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$f$ (Hz)")
    plt.title(r"$f$ for FR")
    apply_style()
    pdf.savefig()
    plt.close()
    
    plt.figure()
    plt.plot(time_stamps, duty_cycles_id2, color='purple', label=r"$d$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$d$ (%)")
    plt.title(r"$d$ for FR")
    apply_style()
    pdf.savefig()
    plt.close()
    
    # Gráfico de Frequência e Duty Cycle para ID 3
    plt.figure()
    plt.plot(time_stamps, frequencies_id3, color='blue', label=r"$f$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$f$ (Hz)")
    plt.title(r"$f$ for SO")
    apply_style()
    pdf.savefig()
    plt.close()
    
    plt.figure()
    plt.plot(time_stamps, duty_cycles_id3, color='blue', label=r"$d$")
    plt.xlabel(r"$t$ (s)")
    plt.ylabel(r"$d$ (%)")
    plt.title(r"$d$ for SO")
    apply_style()
    pdf.savefig()
    plt.close()

print("Gráficos e tabela salvos em cursor_trajectory_plots.pdf e cursor_trajectory_data.csv")