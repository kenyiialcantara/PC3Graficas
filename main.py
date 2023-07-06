import math
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import cv2
import mediapipe as mp

pygame.init()

width = 800
height = 800
size = (width, height)

screen = pygame.display.set_mode(size, DOUBLEBUF | OPENGL | OPENGLBLIT)
gluPerspective(45, (width / height), 0.1, 50.0)
glTranslatef(0.0, 0.0, -5)

background_texture = pygame.image.load('background.jpg')
ganaste_texture = pygame.image.load('Ganaste.png')


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


squares = []

# Círculo (visor)
circle_pos = (0, 0)

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('disparo.wav')


def play_shoot_sound():
    shoot_sound.play()


def generate_square():
    x = random.uniform(-1.5, 1.5)
    y = random.uniform(-1.5, 1.5)
    size = random.uniform(0.1, 0.3)
    # speed_x = random.uniform(-0.01,0.01)
    # speed_y = random.uniform(-0.01, 0.01)
    speed_x = 0.01
    speed_y = 0.01
    return (x, y, size, speed_x, speed_y)


def process_hand_frame(frame):
    # Convertir el fotograma a escala de grises
    imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Crear un objeto de detección de manos de Mediapipe
    mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

    # Detección de manos en el fotograma
    results = mp_hands.process(imgRGB)

    print("results.multi_hand_landmarks", results.multi_hand_landmarks)

    # Imprime la posición de la mano
    if results.multi_hand_landmarks is not None:
        for hand_landmarks in results.multi_hand_landmarks:
            x = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].x
            y = hand_landmarks.landmark[mp.solutions.hands.HandLandmark.WRIST].y
            # Convertir la posición de la mano a coordenadas OpenGL
            norm_x = (x * width / 2) + width / 2
            norm_y = (y * height / 2) + height / 2
            norm_x = (norm_x / width) * 4 - 2
            norm_y = -(norm_y / height) * 4 + 2
            return (norm_x, norm_y)
    return None


# cuadrados iniciales
for _ in range(5):
    squares.append(generate_square())

remaining_squares = len(squares)

cap = cv2.VideoCapture(0)

while True:

    # Capturar frame
    ret, frame = cap.read()

    if not ret:
        break

    # Procesar el fotograma para reconocer la mano y obtener su posición
    hand_pos = process_hand_frame(frame)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 2
            norm_y = -(mouse_y / height) * 4 + 2
            circle_pos = (norm_x, norm_y)

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            norm_x = (mouse_x / width) * 4 - 2
            norm_y = -(mouse_y / height) * 4 + 2

            # Si se hizo clic sobre algún cuadrado y eliminarlo
            for square in squares:
                if norm_x >= square[0] - square[2] and norm_x <= square[0] + square[2] and \
                        norm_y >= square[1] - square[2] and norm_y <= square[1] + square[2]:
                    squares.remove(square)
                    remaining_squares -= 1
                    play_shoot_sound()

    if hand_pos is not None:
        print("aqui")
        mouse_x, mouse_y = hand_pos
        norm_x = mouse_x
        norm_y = -mouse_y
        #norm_x *= 0.75
        #norm_y *= 0.75
        circle_pos = (norm_x, norm_y)

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if remaining_squares == 0:
        draw_background(ganaste_texture)
        # El aviso de "Game Over"
        print('Gameover')
        font = pygame.font.SysFont('serif', 40)
        text = font.render('Game over', False, (1, 1, 1))
        center_x = (width // 2) - (text.get_width() // 2)
        center_y = (height // 2) - (text.get_height() // 2)
        screen.blit(text, [center_x, center_y])
    else:

        draw_background(background_texture)

        # Actualizar la posición de los cuadrados
        for i in range(len(squares)):
            x, y, size, speed_x, speed_y = squares[i]
            x += speed_x
            y += speed_y

            if x + size > 2.5 or x - size < -2.5:
                speed_x *= -1
            if y + size > 2.5 or y - size < -2.5:
                speed_y *= -1
            squares[i] = (x, y, size, speed_x, speed_y)

        # Renderizar los cuadrados en OpenGL
        glBegin(GL_QUADS)
        for square in squares:
            x, y, size, _, _ = square
            r = random.uniform(0, 1)
            g = random.uniform(0, 1)
            b = random.uniform(0, 1)
            glColor3f(r, g, b)
            glVertex3f(x - size, y - size, 0.0)
            glVertex3f(x + size, y - size, 0.0)
            glVertex3f(x + size, y + size, 0.0)
            glVertex3f(x - size, y + size, 0.0)
        glEnd()

        # Draw circle
        glBegin(GL_TRIANGLE_FAN)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(circle_pos[0], circle_pos[1], 0.0)
        for i in range(360):
            degInRad = i * math.pi / 180
            glVertex3f(math.cos(degInRad) * 0.05 + circle_pos[0], math.sin(degInRad) * 0.05 + circle_pos[1], 0.0)
        glEnd()

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()
quit()
