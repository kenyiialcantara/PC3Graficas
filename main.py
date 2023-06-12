
import pygame
import sys
import random
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()

width = 800
height = 600
size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Círculo siguiendo al ratón")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

circle_radius = 20
circle_x = width // 2
circle_y = height // 2

shoot_sound = pygame.mixer.Sound("disparo.wav")

shapes = []

clock = pygame.time.Clock()

def generate_shape():
    shape_type = random.choice(["triangle", "square"])
    x = random.randint(0, width)
    y = random.randint(0, height)
    return {"type": shape_type, "x": x, "y": y}

# Bucle principal del programa
while True:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Clic izquierdo
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for shape in shapes:
                shape_rect = shape["rect"]
                if shape_rect.collidepoint(mouse_x, mouse_y):
                    shapes.remove(shape)
                    shoot_sound.play()  # Reproducir el sonido de disparo

    # Obtener la posición actual del ratón
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Actualizar la posición del círculo para que siga al ratón
    circle_x = mouse_x
    circle_y = mouse_y


    # Generar una nueva figura geométrica aleatoria
    if len(shapes) < 10:  # Limitar la cantidad de figuras en pantalla
        new_shape = generate_shape()
        if new_shape not in shapes:  # Evitar superposiciones
            shapes.append(new_shape)

    # Limpiar la pantalla
    screen.fill(BLACK)

    # Dibujar las figuras geométricas
    for shape in shapes:
        shape_type = shape["type"]
        x = shape["x"]
        y = shape["y"]
        if shape_type == "triangle":
            pygame.draw.polygon(screen, WHITE, [(x, y), (x - 20, y + 40), (x + 20, y + 40)])
        elif shape_type == "square":
            pygame.draw.rect(screen, WHITE, (x - 20, y - 20, 40, 40))
        shape["rect"] = pygame.Rect(x - 20, y - 20, 40, 40)  # Rectángulo colisionador

    # Dibujar el círculo en la nueva posición
    pygame.draw.circle(screen, RED, (circle_x, circle_y), circle_radius)

    # Actualizar la pantalla
    pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(60)
