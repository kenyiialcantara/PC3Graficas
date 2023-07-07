import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLUT import *
import sys
import random
from math import sin, cos, pi

# Lista de cuadrados
squares = []

# Posición del círculo
circle_x = 0.0
circle_y = 0.0

class Square:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.visible = True


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)


def display():
    global circle_x, circle_y

    glClear(GL_COLOR_BUFFER_BIT)

    for square in squares:
        if square.visible:
            glPushMatrix()
            glTranslatef(square.x, square.y, 0.0)

            # Dibujar el cuadrado
            glColor3f(1.0, 0.0, 0.0)
            glBegin(GL_QUADS)
            glVertex2f(-square.size, -square.size)
            glVertex2f(square.size, -square.size)
            glVertex2f(square.size, square.size)
            glVertex2f(-square.size, square.size)
            glEnd()

            glPopMatrix()

    glPushMatrix()
    glTranslatef(circle_x, circle_y, 0.0)

    # Dibujar el círculo
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for i in range(361):
        angle = i * pi / 180.0
        x = 0.2 * cos(angle)
        y = 0.2 * sin(angle)
        glVertex2f(x, y)
    glEnd()

    glPopMatrix()

    pygame.display.flip()


def update():
    global squares

    for square in squares:
        if square.visible:
            # Actualizar la posición del cuadrado
            square.x += square.speed_x
            square.y += square.speed_y

            # Cambiar la dirección si el cuadrado sale de la pantalla
            if square.x + square.size > 1.0 or square.x - square.size < -1.0:
                square.speed_x *= -1
            if square.y + square.size > 1.0 or square.y - square.size < -1.0:
                square.speed_y *= -1

            # Detectar colisión con el círculo
            distance = ((square.x - circle_x) ** 2 + (square.y - circle_y) ** 2) ** 0.5
            if distance <= square.size + 0.2:  # Si hay colisión
                square.visible = False


def main():
    global circle_x, circle_y

    pygame.init()
    pygame.display.set_mode((400, 400), DOUBLEBUF | OPENGL)

    init()

    # Crear 5 cuadrados con velocidades aleatorias
    for _ in range(5):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        size = random.uniform(0.1, 0.3)
        speed_x = random.uniform(-0.01, 0.01)
        speed_y = random.uniform(-0.01, 0.01)
        square = Square(x, y, size, speed_x, speed_y)
        squares.append(square)

    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Actualizar la posición del círculo según la posición del ratón
                circle_x = (event.pos[0] - 200) / 200.0
                circle_y = -(event.pos[1] - 200) / 200.0

        update()
        display()

        clock.tick(60)


if __name__ == "__main__":
    main()