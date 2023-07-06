import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random

# Inicializar Pygame
pygame.init()

# Tamaño de la ventana
width = 800
height = 600

# Crear la ventana
pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

# Configurar OpenGL
glViewport(0, 0, width, height)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluPerspective(45, (width / height), 0.1, 50.0)
glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

# Cargar la imagen de fondo
background_image = pygame.image.load("background.jpg").convert()

# Función para dibujar un cubo
def draw_cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )
    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7)
    )
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

# Generar cubos aleatorios
def generate_cubes(num_cubes):
    cubes = []
    for _ in range(num_cubes):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10)
        dx = random.uniform(-0.1, 0.1)
        dy = random.uniform(-0.1, 0.1)
        dz = random.uniform(-0.1, 0.1)
        cubes.append([(x, y, z), (dx, dy, dz)])
    return cubes

# Cantidad aleatoria de cubos
num_cubes = random.randint(10, 20)
cubes = generate_cubes(num_cubes)

# Bucle principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    glPushMatrix()
    glTranslatef(0, 0, -20)
    glRotatef(1, 3, 1, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar fondo estático
    glPushMatrix()
    glTranslatef(0, 0, -1)
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, background_image.get_width(), background_image.get_height(), 0, GL_RGB,
                 GL_UNSIGNED_BYTE, pygame.image.tostring(background_image, "RGB", 1))
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    tex_w = background_image.get_width()
    tex_h = background_image.get_height()
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(-10, -10, 0)
    glTexCoord2f(0, tex_h)
    glVertex3f(-10, 10, 0)
    glTexCoord2f(tex_w, tex_h)
    glVertex3f(10, 10, 0)
    glTexCoord2f(tex_w, 0)
    glVertex3f(10, -10, 0)
    glEnd()
    glPopMatrix()

    # Dibujar cubos
    for cube in cubes:
        position, velocity = cube
        x, y, z = position
        dx, dy, dz = velocity
        x += dx
        y += dy
        z += dz
        if abs(x) > 10 or abs(y) > 10 or abs(z) > 10:
            x = random.uniform(-10, 10)
            y = random.uniform(-10, 10)
            z = random.uniform(-10, 10)
        cube[0] = (x, y, z)
        glPushMatrix()
        glTranslatef(x, y, z)
        glColor3f(1, 0, 0)  # Color del cubo (rojo)
        draw_cube()
        glPopMatrix()

    pygame.display.flip()
    pygame.time.wait(10)
