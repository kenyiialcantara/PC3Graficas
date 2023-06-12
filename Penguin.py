import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

# Inicializar Pygame
pygame.init()

# Definir el tamaño de la ventana
width = 800
height = 600
size = (width, height)

# Crear la ventana con OpenGL
pygame.display.set_mode(size, DOUBLEBUF | OPENGL)

# Establecer la perspectiva OpenGL
gluPerspective(45, (width / height), 0.1, 50.0)

# Mover la cámara hacia atrás
glTranslatef(0.0, 0.0, -5)

# Bucle principal del programa
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar los pinguinos
    glBegin(GL_TRIANGLES)
    glColor3f(0.0, 0.0, 0.0)  # Color negro
    glVertex3f(0.0, 1.0, 0.0)  # Punto superior
    glVertex3f(-1.0, -1.0, 0.0)  # Punto inferior izquierdo
    glVertex3f(1.0, -1.0, 0.0)  # Punto inferior derecho
    glEnd()

    # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.wait(10)