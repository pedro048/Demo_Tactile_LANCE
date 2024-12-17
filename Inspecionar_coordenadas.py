import matplotlib.pyplot as plt
from PIL import Image

# Caminho para a imagem onde deseja inspecionar os pixels
image_path = "algodao1.jpg"

# Carregar a imagem
img = Image.open(image_path)

# Função para capturar as coordenadas do clique
def onclick(event):
    # Coordenadas x e y
    x, y = int(event.xdata), int(event.ydata)
    print(f"Coordenadas: x={x}, y={y}")

# Exibir a imagem e capturar o clique
fig, ax = plt.subplots()
ax.imshow(img)
fig.canvas.mpl_connect('button_press_event', onclick)
plt.axis("on")
plt.show()