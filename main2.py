from datetime import datetime

import pygame
import sys
from math import sin, cos, pi
from pygame.locals import *
from OpenGL.GL import *
import random
import cv2
import mediapipe as mp
# Definimos la taza de velocidad de cambio de tamanio de los cuadrados
resize_rate=-0.01
# Inicializamos el modulo de la clase que nos permitira importar los sonidos
pygame.mixer.init()
# Cargamos el clip del audio del sonido de disparo
shoot_sound = pygame.mixer.Sound('disparo.wav')
# Definimos la cantidad de cuadrados que crearemos inicialmente con un contador
count = 15
# Instanciamos el objeto de mediapipe para deteccion de manos considerando un confidence bastante holgado
# para asi tener una deteccion más fluida
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
active_background= False
# Definimos las dimensiones a usar
width = 800
height = 800
size = (width, height)

# Cargamos las imagenes usando pygame
background_texture = pygame.image.load('background.jpg')
ganaste_texture = pygame.image.load('Ganaste.png')

# Funcion que permitira reproduccir el sonido del disparo
def play_shoot_sound():
    shoot_sound.play()

# Lista de cuadrados creados durante el juego
squares = []
class Square:
    # Se inicializa con sus coordenadas, su tamanio, y su velocidad de desplazamiento en cada eje
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.visible = True
        self.resize = 0.01
        self.color = (random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1))

# Posición del círculo que simbolizara la mira de disparo
circle_x = 0.0
circle_y = 0.0


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)

# Funcionque repintara la pantalla en cada interacion del bucle principal
def display():
    glClear(GL_COLOR_BUFFER_BIT)
    # Recorremos nuestra lista de cuadrados activos para mostrarlos y trackearlos
    for square in squares:
        if square.visible:
            glPushMatrix()
            glTranslatef(square.x, square.y, 0.0)

            # Dibujar el cuadrado indicando sus colores aleatorios inicializados
            glColor3f(square.color[0], square.color[1],square.color[2])
            glBegin(GL_QUADS)
            # Seteo de las coordenadas de los vertices del cuadrado a dibujar
            glVertex2f(-square.size, -square.size)
            glVertex2f(square.size, -square.size)
            glVertex2f(square.size, square.size)
            glVertex2f(-square.size, square.size)
            glEnd()

            glPopMatrix()

    glPushMatrix()
    glTranslatef(circle_x, circle_y, 0.0)

    # Dibujar el círculo como un poligono de tantos lados que simule un circulo
    glColor3f(0.0, 1.0, 0.0)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0.0, 0.0)
    for i in range(361):
        angle = i * pi / 180.0
        x = 0.1 * cos(angle)
        y = 0.1 * sin(angle)
        glVertex2f(x, y)
    glEnd()

    glPopMatrix()

    pygame.display.flip()



# Funcion encargada de controlar los cambios en cada interacion
def update():
    global count

    # Verificamos todos los cuadrados activos y los dezplazamos acorde a su velocidad respectiva
    for square in squares:
        if square.visible:
            
            # Actualizar la posición del cuadrado
            square.x += square.speed_x
            square.y += square.speed_y

            # Actualizar tamaño del bloque
            square.size+= square.resize

            # Cambiar la dirección si el cuadrado sale de la pantalla simulando rebote
            if square.x + square.size > 1.0 or square.x - square.size < -1.0:
                square.speed_x *= -1
            if square.y + square.size > 1.0 or square.y - square.size < -1.0:
                square.speed_y *= -1
            if square.size > 0.2 or square.size <0.05:
                square.resize = square.resize*-1
                
            # Detectar colisión con el círculo que simboliza la mira
            distance = ((square.x - circle_x) ** 2 + (square.y - circle_y) ** 2) ** 0.5
            if distance <= square.size + 0.1:  # Validar un marguen de cercania considerada colision
                square.visible = False # Ocultar el cuadrado colisionado
                play_shoot_sound()
                count = count - 1 # Actualizar la cantidad de cuadrados activos 



def draw_background(image):
    glEnable(GL_TEXTURE_2D)
    textures = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textures)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    image_data = pygame.image.tostring(image, 'RGBA', 1)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.get_width(), image.get_height(), 0, GL_RGBA, GL_UNSIGNED_BYTE,
                 image_data)

    # Dibujando un plano con la textura de fondo
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

def process_hand_frame(frame):
    # Convertir el fotograma a escala de grises
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Detección de manos con mediapipe en el fotograma pasado de parametro
    results = mp_hands.process(imgRGB)
    # Validar si hubo alguna deteccion de una mano
    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            # Extraer las coordenadas de la deteccion 
            x = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y


            return (800-x*800, y*800)
    return None


def main():

    global circle_x
    global circle_y
    global count
    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    init()

    # Crear cuadrados con parametros aleatorios
    for _ in range(15):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        size = random.uniform(0.1, 0.2)
        speed_x = random.uniform(-0.01, 0.01)
        speed_y = random.uniform(-0.01, 0.01)
        square = Square(x, y, size, speed_x, speed_y)
        squares.append(square)
    # Controlar la velocidad del bucle
    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0) # Activar webCam

    while True:

        # Capturar frame
        ret, frame = cap.read()
        # Hacer inferencia con el modelo de mediapipe
        hand_pos = process_hand_frame(frame)

        if not ret:
            break
        # Redimensionamiento
        frameR = cv2.resize(frame, (800, 800))
        cv2.imshow("Camara", frameR)
        cv2.waitKey(10)

        if hand_pos is not None:
            print("aqui")
            mouse_x, mouse_y = hand_pos
            # norm_x *= 0.75
            # norm_y *= 0.75
            circle_pos = (mouse_x, mouse_y)
            print(circle_pos)
            # Extraer coordenadas del mouse
            mouse_x, mouse_y = circle_pos
            # circle_x = (mouse_x / width) * 4 - 2
            # circle_y = -(mouse_y / height) * 4 + 2
            # Ajustar normalizando posiciones para el circulo
            circle_x = (mouse_x - 400) / 400.0
            circle_y = -(mouse_y - 400) / 400.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Actualizar la posición del círculo según la posición del ratón
                circle_x = (event.pos[0] - 400) / 400.0
                circle_y = -(event.pos[1] - 400) / 400.0

        print(count)
        if count <= 0:
            # draw_background(ganaste_texture)
            # El aviso de "Game Over"
            print('Gameover')
            font = pygame.font.SysFont('serif', 40)
            text = font.render('Game over', False, (1, 1, 1))
            center_x = (width // 2) - (text.get_width() // 2)
            center_y = (height // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])
            break
        update()
        display()
        # Control de iteraciones para evitar crasheo
        clock.tick(60)





def GameOver():

    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    init()
    clock = pygame.time.Clock()

    # sacar la hora actual y sumarle 60 segundos
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    print("Current Time =", current_time)

    if now.second >= 30:
        timeAdded = now.replace(minute=now.minute + 1)
        timeAdded = timeAdded.replace(second=now.second - 30)
    else:
        timeAdded = now.replace(second=now.second + 30)

    # timeAdded = now.replace(minute=now.minute+1)
    timeAddedStr = timeAdded.strftime("%H:%M:%S")
    print("Time Added =", timeAddedStr)

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Actualizar la posición del círculo según la posición del ratón
                circle_x = (event.pos[0] - 400) / 400.0
                circle_y = -(event.pos[1] - 400) / 400.0




        print('Gameover')
        draw_background(ganaste_texture)
        print('Gameover')
        font = pygame.font.SysFont('serif', 40)
        text = font.render('Game over', False, (1, 1, 1))
        center_x = (width // 2) - (text.get_width() // 2)
        center_y = (height // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])



        nowLoop = datetime.now()
        current_time = nowLoop.strftime("%H:%M:%S")
        print("Current Time =", current_time)
        if nowLoop > timeAdded:
            print("Fin del juego")
            break

        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
    GameOver()

