import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width = 800
height = 800
size = (width, height)

# Crear la ventana con OpenGL
pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

# Establecer la perspectiva OpenGL
gluPerspective(45, (width / height), 0.1, 50.0)

# Mover la cámara hacia atrás
glTranslatef(0.0, 0.0, -5)

# Lista para almacenar los cuadrados
squares = []

# Círculo que sigue la posición del ratón
circle_pos = (0, 0)

# Cargar el sonido de disparo
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('disparo.wav')


# Función para reproducir el sonido de disparo
def play_shoot_sound():
    shoot_sound.play()


# Función para generar un cuadrado aleatorio
def generate_square():
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    size = random.uniform(0.1, 0.3)
    return (x, y, size)


# Generar cuadrados iniciales
for _ in range(5):
    squares.append(generate_square())

# Bucle principal del programa
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.MOUSEMOTION:
            # Obtener la posición del ratón y convertirla a coordenadas OpenGL
            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 1
            norm_y = -(mouse_y / height) * 4 + 1
            circle_pos = (norm_x, norm_y)
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del clic del ratón y convertirla a coordenadas OpenGL
            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 1
            norm_y = -(mouse_y / height) * 4 + 1

            # Buscar si se hizo clic sobre algún cuadrado y eliminarlo
            for square in squares:
                if norm_x >= square[0] - square[2] and norm_x <= square[0] + square[2] and \
                        norm_y >= square[1] - square[2] and norm_y <= square[1] + square[2]:
                    squares.remove(square)
                    play_shoot_sound()

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Renderizar los cuadrados en OpenGL
    glBegin(GL_QUADS)
    for square in squares:
        x, y, size = square
        glVertex3f(x - size, y - size, 0.0)
        glVertex3f(x + size, y - size, 0.0)
        glVertex3f(x + size, y + size, 0.0)
        glVertex3f(x - size, y + size, 0.0)
    glEnd()

    # Dibujar el círculo que sigue la posición del ratón
    glColor3f(1.0, 1.0, 1.0)  # Color blanco
    glPushMatrix()
    glTranslatef(circle_pos[0], circle_pos[1], 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(0.0, 0.0, 0.0)
    num_segments = 100  # Número de segmentos para el círculo
    for i in range(num_segments + 1):
        theta = (2.0 * 3.1415926) * (float(i) / num_segments)
        x = 0.1 * float(math.cos(theta))
        y = 0.1 * float(math.sin(theta))
        glVertex3f(x, y, 0.0)
    glEnd()
    glPopMatrix()

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.wait(10)
