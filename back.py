import pygame
import sys
from math import sin, cos, pi
from pygame.locals import *
from OpenGL.GL import *
import random
import cv2
import mediapipe as mp


background_texture = pygame.image.load('background.jpg')
ganaste_texture = pygame.image.load('Ganaste.png')

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('disparo.wav')

# Crear un objeto de detección de manos de Mediapipe
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)
active_background= False
width = 800
height = 800
size = (width, height)


def play_shoot_sound():
    shoot_sound.play()

# Lista de cuadrados
squares = []
class Square:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.x = x
        self.y = y
        self.size = size
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.visible = True
        self.color = (random.uniform(0, 1),random.uniform(0, 1),random.uniform(0, 1))

# Posición del círculo
circle_x = 0.0
circle_y = 0.0

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


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    for square in squares:
        if square.visible:
            glPushMatrix()
            glTranslatef(square.x, square.y, 0.0)

            # Dibujar el cuadrado
            glColor3f(square.color[0], square.color[1],square.color[2])
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
        x = 0.1 * cos(angle)
        y = 0.1 * sin(angle)
        glVertex2f(x, y)
    glEnd()

    glPopMatrix()

    pygame.display.flip()


count = 5

def update():
    global count

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
            if distance <= square.size + 0.1:  # Si hay colisión
                square.visible = False
                play_shoot_sound()
                count = count - 1



def process_hand_frame(frame):
    # Convertir el fotograma a escala de grises
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


    # Detección de manos en el fotograma
    results = mp_hands.process(imgRGB)
    # Imprime la posición de la mano
    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].x
            y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y
            # Convertir la posición de la mano a coordenadas OpenGL

            return (800-x*800, y*800)
    return None


def main():

    global circle_x
    global circle_y
    global count
    pygame.init()
    screen = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)

    init()

    # Crear 5 cuadrados con velocidades aleatorias
    for _ in range(15):
        x = random.uniform(-1.0, 1.0)
        y = random.uniform(-1.0, 1.0)
        size = random.uniform(0.1, 0.2)
        speed_x = random.uniform(-0.01, 0.01)
        speed_y = random.uniform(-0.01, 0.01)
        square = Square(x, y, size, speed_x, speed_y)
        squares.append(square)

    clock = pygame.time.Clock()
    cap = cv2.VideoCapture(0)

    while True:

        # # Capturar frame
        ret, frame = cap.read()
        hand_pos = process_hand_frame(frame)

        if not ret:
            break
        # frameR = cv2.resize(frame, (800, 800))
        # cv2.imshow("Camara", frameR)
        # cv2.waitKey(10)

        if hand_pos is not None:
            print("aqui")
            mouse_x, mouse_y = hand_pos
            # norm_x *= 0.75
            # norm_y *= 0.75
            circle_pos = (mouse_x, mouse_y)
            print(circle_pos)

            # Handle shooting action when space key is released
            # Get the mouse position
            mouse_x, mouse_y = circle_pos
            # Convert mouse position to normalized coordinates
            # circle_x = (mouse_x / width) * 4 - 2
            # circle_y = -(mouse_y / height) * 4 + 2
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

        if count == 0:
            # draw_background(ganaste_texture)
            # El aviso de "Game Over"
            print('Gameover')
            font = pygame.font.SysFont('serif', 40)
            text = font.render('Game over', False, (1, 1, 1))
            center_x = (width // 2) - (text.get_width() // 2)
            center_y = (height // 2) - (text.get_height() // 2)
            screen.blit(text, [center_x, center_y])

        update()
        display()

        clock.tick(60)


if __name__ == "__main__":
    main()
