from OpenGL.raw.GLU import gluPerspective
from pygame.locals import *
from glApp.LoadMesh import *

vertex_shader = r'''
#version 330 core
in vec3 position;
in vec3 vertex_color;
uniform mat4 projection_mat;
uniform mat4 model_mat;
uniform mat4 view_mat;
out vec3 color;
void main()
{
    gl_Position = projection_mat * inverse(view_mat) * model_mat * vec4(position,1);
    color = vertex_color;
}
'''

fragment_shader = r'''
#version 330 core
in vec3 color;
out vec4 frag_color;
void main()
{
    frag_color = vec4(color, 1);
}
'''

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

# Cargar el sonido de disparo
pygame.mixer.init()
disparo_sound = pygame.mixer.Sound("disparo.wav")

# Cargar el archivo OBJ del pingüino
# pinguino_mesh = Wavefront("11706_stuffed_animal_L2.obj")
program_id = create_program(vertex_shader, fragment_shader)
pinguino_mesh =LoadMesh('11706_stuffed_animal_L2.obj',program_id)

# Lista de pingüinos
pinguinos = []

# Generar pingüinos iniciales
for _ in range(10):
    x = random.uniform(-2.0, 2.0)
    y = random.uniform(-2.0, 2.0)
    z = random.uniform(-2.0, 2.0)
    pinguinos.append({"x": x, "y": y, "z": z})

# Bucle principal del programa
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Clic izquierdo
                disparo_sound.play()

                # Obtener la posición del clic en la ventana
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Convertir las coordenadas de la ventana a coordenadas OpenGL
                viewport = glGetIntegerv(GL_VIEWPORT)
                mouse_x = (mouse_x / viewport[2]) * 2 - 1
                mouse_y = -(mouse_y / viewport[3]) * 2 + 1

                # Verificar si el clic alcanza algún pingüino
                for pinguino in pinguinos:
                    pinguino_x = pinguino["x"]
                    pinguino_y = pinguino["y"]
                    pinguino_z = pinguino["z"]
                    if mouse_x >= pinguino_x - 0.5 and mouse_x <= pinguino_x + 0.5 and mouse_y >= pinguino_y - 0.5 and mouse_y <= pinguino_y + 0.5:
                        pinguinos.remove(pinguino)
                        break

    # Limpiar la pantalla
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Dibujar los pingüinos
    for pinguino in pinguinos:
        x = pinguino["x"]
        y = pinguino["y"]
        z = pinguino["z"]
        glPushMatrix()
        glTranslatef(x, y, z)
        glScalef(0.1, 0.1, 0.1)  # Escalar el pingüino

        # Dibujar el pingüino
        pinguino_mesh.draw()
        for mesh in pinguino_mesh.mesh_list:
            pinguino_mesh.draw()
            # glBegin(GL_TRIANGLES)
            # for face in mesh.faces:
            #     for vertex_i in face:
            #         vertex = mesh.vertices[vertex_i]
            #         normal = mesh.normals[vertex_i]
            #         glNormal3f(*normal)
            #         glVertex3f(*vertex)

            glEnd()

        glPopMatrix()

        # Actualizar la pantalla
    pygame.display.flip()
    pygame.time.wait(10)