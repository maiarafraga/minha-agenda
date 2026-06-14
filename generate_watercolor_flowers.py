#!/usr/bin/env python3
"""
Gerador de flores em aquarela para app feminino
Cria assets com fundo transparente, estilo devocional/papelaria fina
"""

from PIL import Image, ImageDraw
import random
import math

# Configuração de cores
COLORS = {
    "rose_dark": (215, 125, 155, 180),      # Rosa escuro - transparente
    "rose_light": (235, 165, 190, 150),     # Rosa claro - mais transparente
    "blush": (245, 195, 210, 140),          # Blush - muito transparente
    "coral": (235, 140, 130, 160),          # Coral suave
    "peach": (245, 180, 160, 130),          # Pêssego
    "green_sage": (140, 165, 140, 140),     # Verde sage
    "green_light": (170, 190, 160, 120),    # Verde claro
    "gold": (220, 180, 100, 180),           # Dourado
    "cream": (255, 250, 245, 80),           # Creme muito transparente
}

def draw_watercolor_circle(draw, x, y, radius, color, num_layers=4):
    """Desenha um círculo com efeito aquarela (múltiplas camadas com fade)"""
    for i in range(num_layers, 0, -1):
        r = radius * (i / num_layers)
        alpha = color[3] * (1 - (i / num_layers) * 0.7)
        layer_color = (color[0], color[1], color[2], int(alpha))
        draw.ellipse(
            [x - r, y - r, x + r, y + r],
            fill=layer_color
        )

def draw_petal(draw, center_x, center_y, angle, petal_length, petal_width, color):
    """Desenha uma pétala com efeito aquarela"""
    # Converter ângulo para radianos
    rad = math.radians(angle)

    # Ponto final da pétala
    end_x = center_x + petal_length * math.cos(rad)
    end_y = center_y + petal_length * math.sin(rad)

    # Desenhar com múltiplos círculos para efeito aquarela
    steps = int(petal_length / 5)
    for i in range(steps):
        progress = i / steps
        x = center_x + progress * (end_x - center_x)
        y = center_y + progress * (end_y - center_y)
        r = petal_width * (1 - progress * 0.3)
        alpha = color[3] * (1 - progress * 0.5)
        layer_color = (color[0], color[1], color[2], int(alpha))
        draw.ellipse(
            [x - r/2, y - r/2, x + r/2, y + r/2],
            fill=layer_color
        )

def draw_flower(draw, center_x, center_y, flower_size=40, petal_color=None, center_color=None):
    """Desenha uma flor completa com pétalas e centro"""
    if petal_color is None:
        petal_color = random.choice([COLORS["rose_light"], COLORS["blush"], COLORS["coral"]])
    if center_color is None:
        center_color = COLORS["gold"]

    # Desenhar pétalas (6 pétalas)
    num_petals = 5 + random.randint(0, 2)
    for i in range(num_petals):
        angle = (360 / num_petals) * i + random.randint(-15, 15)
        petal_length = flower_size * random.uniform(0.8, 1.2)
        petal_width = flower_size * 0.4
        draw_petal(draw, center_x, center_y, angle, petal_length, petal_width, petal_color)

    # Desenhar centro
    draw_watercolor_circle(draw, center_x, center_y, flower_size * 0.25, center_color, num_layers=3)

def draw_leaf(draw, center_x, center_y, angle, leaf_size, color):
    """Desenha uma folha em estilo aquarela"""
    rad = math.radians(angle)

    # Ponto final da folha
    end_x = center_x + leaf_size * math.cos(rad)
    end_y = center_y + leaf_size * math.sin(rad)

    # Desenhar com pontos para efeito aquarela
    steps = int(leaf_size / 3)
    for i in range(steps):
        progress = i / steps
        x = center_x + progress * (end_x - center_x)
        y = center_y + progress * (end_y - center_y)
        r = (leaf_size * 0.15) * (1 - progress * 0.4)
        alpha = color[3] * (1 - progress * 0.3)
        layer_color = (color[0], color[1], color[2], int(alpha))
        draw.ellipse(
            [x - r/2, y - r/2, x + r/2, y + r/2],
            fill=layer_color
        )

def draw_leaf_cluster(draw, center_x, center_y, num_leaves=3, leaf_size=30):
    """Desenha um aglomerado de folhas"""
    for i in range(num_leaves):
        angle = 60 + (i * 45) + random.randint(-20, 20)
        leaf_color = random.choice([COLORS["green_sage"], COLORS["green_light"]])
        draw_leaf(draw, center_x, center_y, angle, leaf_size, leaf_color)

def generate_horizontal_banner(width=1600, height=500):
    """Gera guirlanda floral horizontal para header"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')

    # Flores concentradas nos cantos e no centro
    flower_positions = [
        # Esquerda
        (150, 150), (200, 250), (120, 350),
        # Centro-esquerda
        (500, 120), (600, 300), (550, 400),
        # Centro
        (800, 100), (800, 450),
        # Centro-direita
        (1050, 150), (1100, 350),
        # Direita
        (1400, 200), (1480, 280), (1450, 380),
    ]

    # Desenhar folhagem de fundo
    for x in range(50, width, 200):
        for y in range(50, height, 150):
            if random.random() > 0.3:
                draw_leaf_cluster(draw, x + random.randint(-30, 30), y + random.randint(-30, 30), num_leaves=2, leaf_size=20)

    # Desenhar flores principais
    for x, y in flower_positions:
        flower_size = random.uniform(30, 50)
        petal_color = random.choice([
            COLORS["rose_light"],
            COLORS["blush"],
            COLORS["coral"],
            COLORS["peach"]
        ])
        draw_flower(draw, x, y, flower_size=flower_size, petal_color=petal_color)

        # Adicionar folhas ao redor de algumas flores
        if random.random() > 0.4:
            draw_leaf_cluster(draw, x + random.randint(-40, 40), y + random.randint(-40, 40), num_leaves=random.randint(2, 4), leaf_size=25)

    # Adicionar respingos de dourado
    for _ in range(15):
        x = random.randint(0, width)
        y = random.randint(0, height)
        radius = random.uniform(2, 6)
        gold_alpha = COLORS["gold"][3] * random.uniform(0.3, 1.0)
        gold_color = (COLORS["gold"][0], COLORS["gold"][1], COLORS["gold"][2], int(gold_alpha))
        draw_watercolor_circle(draw, x, y, radius, gold_color, num_layers=2)

    return img

def generate_corner_cluster(width=700, height=700):
    """Gera buquê de canto para decoração"""
    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, 'RGBA')

    center_x, center_y = width * 0.6, height * 0.6

    # Folhagem de fundo - base do buquê
    for i in range(8):
        angle = 45 * i + random.randint(-20, 20)
        draw_leaf_cluster(draw, center_x, center_y, num_leaves=3, leaf_size=50)

    # Primeira camada de flores (maiores, atrás)
    for i in range(3):
        offset_angle = random.uniform(0, 360)
        offset_distance = random.uniform(40, 80)
        x = center_x + offset_distance * math.cos(math.radians(offset_angle))
        y = center_y + offset_distance * math.sin(math.radians(offset_angle))

        petal_color = random.choice([
            COLORS["rose_dark"],
            COLORS["rose_light"],
            COLORS["coral"]
        ])
        draw_flower(draw, x, y, flower_size=45, petal_color=petal_color)

    # Segunda camada de flores (médias, meio)
    for i in range(4):
        offset_angle = random.uniform(0, 360)
        offset_distance = random.uniform(30, 60)
        x = center_x + offset_distance * math.cos(math.radians(offset_angle))
        y = center_y + offset_distance * math.sin(math.radians(offset_angle))

        petal_color = random.choice([
            COLORS["blush"],
            COLORS["peach"],
            COLORS["rose_light"]
        ])
        draw_flower(draw, x, y, flower_size=35, petal_color=petal_color)

    # Terceira camada de flores (pequenas, frente)
    for i in range(4):
        offset_angle = random.uniform(0, 360)
        offset_distance = random.uniform(15, 45)
        x = center_x + offset_distance * math.cos(math.radians(offset_angle))
        y = center_y + offset_distance * math.sin(math.radians(offset_angle))

        petal_color = random.choice([
            COLORS["rose_light"],
            COLORS["blush"],
            COLORS["cream"]
        ])
        draw_flower(draw, x, y, flower_size=28, petal_color=petal_color)

    # Adicionar detalhes de dourado e pontos delicados
    for _ in range(12):
        x = center_x + random.randint(-150, 150)
        y = center_y + random.randint(-150, 150)
        radius = random.uniform(1.5, 4)
        gold_alpha = COLORS["gold"][3] * random.uniform(0.4, 0.9)
        gold_color = (COLORS["gold"][0], COLORS["gold"][1], COLORS["gold"][2], int(gold_alpha))
        draw_watercolor_circle(draw, x, y, radius, gold_color, num_layers=2)

    return img

if __name__ == "__main__":
    print("Gerando guirlanda floral horizontal (header)...")
    banner = generate_horizontal_banner()
    banner.save("/Users/maiarafraga/agenda-deploy/assets/flores-topo.png", "PNG")
    print("✓ Salvo: /Users/maiarafraga/agenda-deploy/assets/flores-topo.png (1600x500)")

    print("Gerando buquê de canto...")
    corner = generate_corner_cluster()
    corner.save("/Users/maiarafraga/agenda-deploy/assets/flores-canto.png", "PNG")
    print("✓ Salvo: /Users/maiarafraga/agenda-deploy/assets/flores-canto.png (700x700)")

    print("\n✅ Assets gerados com sucesso!")
