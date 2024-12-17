from PIL import Image, ImageDraw, ImageFont
import matplotlib.pyplot as plt

# Função para desenhar a trajetória, nomear pontos em bolinhas vermelhas e adicionar placas em quadrados brancos
def draw_trajectory_on_image(image_path, points, labels, placas):
    # Carrega a imagem indicada
    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)
    
    # Definir fonte padrão do sistema, se disponível
    try:
        font = ImageFont.truetype("arial.ttf", 14)  # Fonte Arial para Windows
    except IOError:
        font = ImageFont.load_default()  # Fonte padrão se Arial não estiver disponível
    
    # Desenha as linhas de trajetória e marca os pontos
    for i in range(len(points) - 1):
        draw.line((points[i], points[i + 1]), fill="black", width=3)  # Linha preta para a trajetória
    
    # Marcar cada ponto e adicionar as etiquetas em bolinhas vermelhas com texto branco
    for i, (x, y) in enumerate(points):
        # Desenhar a bolinha vermelha
        draw.ellipse((x - 10, y - 10, x + 10, y + 10), fill="red")
        
        # Centralizar o texto dentro da bolinha
        text_bbox = draw.textbbox((0, 0), labels[i], font=font)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        
        text_x = x - text_w // 2
        text_y = y - text_h // 2
        draw.text((text_x, text_y), labels[i], fill="white", font=font)
    
    # Adicionar as placas próximas aos grupos de pontos em quadrados brancos
    for placa, pontos_assoc in placas:
        # Calcular uma média de posição para a placa próxima ao grupo de pontos
        avg_x = sum(points[i][0] for i in pontos_assoc) // len(pontos_assoc)
        avg_y = sum(points[i][1] for i in pontos_assoc) // len(pontos_assoc)
        
        # Ajustar a posição para a placa "SO" entre os pontos B e C
        if placa == "SO" and pontos_assoc == [1, 2]:
            avg_x -= 20  # Desloca 20 pixels para a esquerda (ajuste conforme necessário)
        
        # Calcular a posição do quadrado branco para a placa
        text_bbox = draw.textbbox((0, 0), placa, font=font)
        text_w, text_h = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]
        
        rect_x0, rect_y0 = avg_x + 8, avg_y - 12
        rect_x1, rect_y1 = rect_x0 + text_w + 6, rect_y0 + text_h + 4
        draw.rectangle([rect_x0, rect_y0, rect_x1, rect_y1], fill="white")

        # Adicionar o nome da placa (SO, FR, CR, AoC) dentro do quadrado branco
        draw.text((rect_x0 + 3, rect_y0), placa, fill="black", font=font)
    
    return img

# Coordenadas dos pontos (x, y) e seus rótulos, com o novo ponto F adicionado e os demais ajustados
points = [
    (143, 412),  # Ponto A
    (143, 231),  # Ponto B
    (197, 231),  # Ponto C   
    (197, 410),  # Ponto D
    (307, 410),  # Ponto E
    (278, 205),  # Novo Ponto F
    (262, 106),  # Ponto G (anteriormente F)
    (226, 30),   # Ponto H (anteriormente G)
    (192, 89)    # Ponto I (anteriormente H)
]
labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I']

# Atualização das placas com as novas posições usando uma lista de tuplas (placa, [pontos associados])
placas = [
    ("SO", [0, 1]),        # Placa SO entre os pontos A e B
    ("SO", [1, 2]),        # Nova placa SO entre os pontos B e C
    ("FR", [1, 2, 3]),     # Placa FR entre os pontos B, C, D
    ("CR", [6, 7]),        # Placa CR entre os pontos G e H
    ("SO", [3, 4]),        # Outra placa SO entre os pontos D e E
    ("AoS", [5, 6]),       # Placa AoC entre os pontos F e G
    ("SO", [4, 5]),        # Nova placa SO entre os pontos E e F
    ("CR", [7, 8])         # Nova placa CR entre os pontos H e I
]

# Caminho para a imagem onde será desenhada a trajetória
image_path = "algodao1.jpg"

# Carregar a imagem e desenhar a trajetória, os pontos e as placas
img_with_trajectory = draw_trajectory_on_image(image_path, points, labels, placas)

# Exibir a imagem final com os trajetos, pontos e placas
plt.figure(figsize=(10, 8))
plt.imshow(img_with_trajectory)
plt.axis("off")
plt.show()