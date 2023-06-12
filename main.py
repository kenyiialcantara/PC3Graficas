import math

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

pygame.init()

width = 800
height = 600
size = (width, height)

#ventana con OpenGL
screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

# Perspectiva OpenGL
gluPerspective(45, (width / height), 0.1 , 50.0)

# Mover la cámara hacia atrás
glTranslatef(0.0, 0.0, -5)

# fondo
background_texture = pygame.image.load('background.jpg')

def draw_background():

    glEnable(GL_TEXTURE_2D)
    textures = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image_data = pygame.image.tostring(background_texture, 'RGBA', 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, background_texture.get_width(), background_texture.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)

    # Dibujar un plano con la textura de fondo
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 0.0)
    glVertex3f(-2.5, -2.5, -1.0)
    glTexCoord2f(1.0, 0.0)
    glVertex3f(2.5, -2.5, -1.0)
    glTexCoord2f(1.0, 1.0)
    glVertex3f(2.5, 2.5, -1.0)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-2.5, 2.5, -1.0)
    glEnd()

    glDisable(GL_TEXTURE_2D)

# Lista para almacenar los cuadrados
squares = []

# Círculo (visor)
circle_pos = (0, 0)

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('disparo.wav')

def play_shoot_sound():
    shoot_sound.play()

# generar un cuadrado aleatorio
def generate_square():
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    size = random.uniform(0.1, 0.3)
    # speed_x = random.uniform(-0.01,0.01)
    # speed_y = random.uniform(-0.01, 0.01)
    speed_x = 0.01
    speed_y = 0.01
    return (x, y, size, speed_x, speed_y)

# cuadrados iniciales
for _ in range(5):
    squares.append(generate_square())


remaining_squares = len(squares) #Para contar los cuadrados (Sirve para el gameover )

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        # Obtener la posición del ratón y click, y convertirla a coordenadas OpenGL
        if event.type == pygame.MOUSEMOTION:

            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 1
            norm_y = -(mouse_y / height) * 4 + 1
            circle_pos = (norm_x, norm_y)
        if event.type == pygame.MOUSEBUTTONDOWN:

            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 1
            norm_y = -(mouse_y / height) * 4 + 1

            # Si se hizo clic sobre algún cuadrado y eliminarlo
            for square in squares:
                if norm_x >= square[0] - square[2] and norm_x <= square[0] + square[2] and \
                   norm_y >= square[1] - square[2] and norm_y <= square[1] + square[2]:
                    squares.remove(square)
                    remaining_squares -= 1 #Disminuir el numero de cuadrados
                    print(remaining_squares)
                    play_shoot_sound()

    # Clean la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if remaining_squares == 0:
        # El aviso de "Game Over"
        print('Gameover')
        font = pygame.font.SysFont('serif', 40)
        text = font.render('Game over',False,(1,1,1))
        center_x = (width//2) - (text.get_width()//2)
        center_y = (height//2) - (text.get_height()//2)
        screen.blit(text, [center_x,center_y])
    else:

        draw_background()

        # Actualizar la posición de los cuadrados
        for i in range(len(squares)):
            x, y, size, speed_x, speed_y = squares[i]
            x += speed_x
            y += speed_y
            # Límites de la pantalla
            if x + size > 2.5 or x - size < -2.5:
                speed_x *= -1
            if y + size > 2.5 or y - size < -2.5:
                speed_y *= -1
            squares[i] = (x, y, size, speed_x, speed_y)

        # Renderizar los cuadrados en OpenGL
        glBegin(GL_QUADS)
        for square in squares:
            x, y, size, _, _ = square
            glColor3f(1.0, 0.0, 0.0)  # Color rojo
            glVertex3f(x - size, y - size, 0.0)
            glVertex3f(x + size, y - size, 0.0)
            glVertex3f(x + size, y + size, 0.0)
            glVertex3f(x - size, y + size, 0.0)
        glEnd()


        # Draw círculo que sigue la posición del ratón
        glColor3f(1.0, 1.0, 1.0)
        glPushMatrix()
        glTranslatef(circle_pos[0], circle_pos[1], 0.0)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(0.0, 0.0, 0.0)
        num_segments = 100
        for i in range(num_segments + 1):
            theta = (2.0 * 3.1415926) * (float(i) / num_segments)
            x = 0.1 * float(math.cos(theta))
            y = 0.1 * float(math.sin(theta))
            glVertex3f(x, y, 0.0)

        glEnd()
        glPopMatrix()

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.wait(60)

