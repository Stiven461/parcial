# pylint: disable=E1101

import pygame
import pygame_gui
import math

# Inicialización de Pygame y Pygame GUI
pygame.init()
pygame.display.set_caption("Simulación de Carrito con Dos Ruedas")

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Tamaño de la ventana
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Crear el gestor de interfaz de Pygame GUI
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Crear campos de entrada para voltajes y botones
voltaje_izq_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((10, 10), (150, 30)),
    manager=manager
)

# Etiqueta para el voltaje izquierdo
voltaje_izq_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((150, 10), (50, 30)),
    text='V.I',
    manager=manager
)

voltaje_der_input = pygame_gui.elements.UITextEntryLine(
    relative_rect=pygame.Rect((10, 50), (150, 30)),
    manager=manager
)

# Etiqueta para el voltaje derecho
voltaje_der_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((150, 50), (50, 30)),
    text='V.D',
    manager=manager
)

apply_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 90), (150, 30)),
    text='Aplicar Voltajes',
    manager=manager
)

reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 130), (150, 30)),
    text='Restablecer',
    manager=manager
)

# Parámetros del carrito
x, y = WIDTH // 2, HEIGHT // 2
angle = 0
largo = 50
ancho = 30
tamaño_rueda = 8
voltaje_izquierdo = 0
voltaje_derecho = 0

# Crear superficie para el carrito
carrito_surface = pygame.Surface((largo, ancho))
carrito_surface.fill(RED)
carrito_surface.set_colorkey(WHITE)

# Funciones para actualizar la posición y ángulo del carrito
def mover_carrito(voltaje_izquierdo, voltaje_derecho):
    global x, y, angle
    velocidad_promedio = (voltaje_izquierdo + voltaje_derecho) / 2

    if voltaje_izquierdo == voltaje_derecho:
        # Movimiento hacia adelante o hacia atrás
        dx = velocidad_promedio * math.cos(math.radians(angle))
        dy = -velocidad_promedio * math.sin(math.radians(angle))
        
        # Verificar colisiones con los bordes
        if (0 <= x + dx - largo // 2 and x + dx + largo // 2 <= WIDTH):
            x += dx
        if (0 <= y + dy - ancho // 2 and y + dy + ancho // 2 <= HEIGHT):
            y += dy
    else:
        # Si voltajes son diferentes, el carrito gira
        angle_cambio = (voltaje_derecho - voltaje_izquierdo) / 20
        angle += angle_cambio
        dx = velocidad_promedio * math.cos(math.radians(angle))
        dy = -velocidad_promedio * math.sin(math.radians(angle))
        
        # Verificar colisiones con los bordes
        if (0 <= x + dx - largo // 2 and x + dx + largo // 2 <= WIDTH):
            x += dx
        if (0 <= y + dy - ancho // 2 and y + dy + ancho // 2 <= HEIGHT):
            y += dy

def mover_carrito_a_punto(destino_x, destino_y, velocidad):
    global x, y, angle
    dx = destino_x - x
    dy = destino_y - y
    distancia = math.hypot(dx, dy)

    if distancia > velocidad:
        angulo_destino = math.degrees(math.atan2(-dy, dx))
        angle = angulo_destino
        x += velocidad * math.cos(math.radians(angulo_destino))
        y -= velocidad * math.sin(math.radians(angulo_destino))
        return False
    else:
        x, y = destino_x, destino_y
        return True
 

# Dibuja el carrito en la pantalla
def dibujar_carrito():
    rotated_surface = pygame.transform.rotate(carrito_surface, angle)
    new_rect = rotated_surface.get_rect(center=(x, y))
    window.blit(rotated_surface, new_rect.topleft)
    
    distancia_ruedas = largo // 2 - 5
    rueda_izq_x = x - distancia_ruedas * math.sin(math.radians(angle))
    rueda_izq_y = y - distancia_ruedas * math.cos(math.radians(angle))
    rueda_der_x = x + distancia_ruedas * math.sin(math.radians(angle))
    rueda_der_y = y + distancia_ruedas * math.cos(math.radians(angle))
    
    pygame.draw.rect(window, GRAY, (rueda_izq_x - tamaño_rueda // 2, rueda_izq_y - tamaño_rueda // 2, tamaño_rueda, tamaño_rueda))
    pygame.draw.rect(window, GRAY, (rueda_der_x - tamaño_rueda // 2, rueda_der_y - tamaño_rueda // 2, tamaño_rueda, tamaño_rueda))


# Bucle principal del juego
clock = pygame.time.Clock()
running = True
while running:
    time_delta = clock.tick(30) / 1000.0
    window.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == apply_button:
                try:
                    voltaje_izquierdo = float(voltaje_izq_input.get_text())
                    voltaje_derecho = float(voltaje_der_input.get_text())
                except ValueError:
                    pass

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == reset_button:
                voltaje_izquierdo = 0
                voltaje_derecho = 0
                x, y = WIDTH // 2, HEIGHT // 2
                angle = 0
                voltaje_izq_input.set_text('')
                voltaje_der_input.set_text('')

    mover_carrito(voltaje_izquierdo, voltaje_derecho)
    dibujar_carrito()
    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.flip()

pygame.quit()