# pylint: disable=E1101

import pygame
import pygame_gui
import math
import random  # Importar random para generar posiciones aleatorias

# Inicialización de Pygame y Pygame GUI
pygame.init()
pygame.display.set_caption("Simulación de Carrito con Dos Ruedas")

# Definir colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLUE = (0, 0, 255)

# Tamaño de la ventana
WIDTH, HEIGHT = 600, 600
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

# Agregar menú desplegable para seleccionar la figura
dropdown_menu = pygame_gui.elements.UIDropDownMenu(
    options_list=['Selecciona una figura', 'Círculo', 'Triángulo', 'Cuadrado', 'Pentágono', 'Hexágono', 'Heptágono', 'Octágono', 'Decágono', 'Dodecágono'],
    starting_option='Selecciona una figura',
    relative_rect=pygame.Rect((10, 170), (150, 30)),
    manager=manager
)

# Crear botón para recorrer el área
espiral_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 210), (150, 30)),
    text='Recorrer Área',
    manager=manager
)

# Agregar botón para generar obstáculos
obstaculos_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 250), (150, 30)),
    text='Generar Obstáculos',
    manager=manager
)

# Parámetros del carrito
x, y = WIDTH // 2, HEIGHT // 2
angle = 90  # El carrito inicialmente apunta hacia el norte (90 grados)
largo = 40
ancho = 20
tamaño_rueda = 6
voltaje_izquierdo = 0
voltaje_derecho = 0
figure_selected = None
poligono_vertices = []
vertice_actual = 0
rastro = []

# Lista para almacenar obstáculos
obstaculos = []

# Crear superficie para el carrito
carrito_surface = pygame.Surface((largo, ancho))
carrito_surface.fill(RED)
carrito_surface.set_colorkey(WHITE)

# Función para calcular los vértices de la figura seleccionada
def calcular_poligono(lados, radio):
    global x, y
    puntos = []
    for i in range(lados):
        angulo = i * 2 * math.pi / lados
        px = x + radio * math.cos(angulo)
        py = y + radio * math.sin(angulo)
        puntos.append((px, py))
    return puntos

# Funciones para actualizar la posición y ángulo del carrito
def mover_carrito(voltaje_izquierdo, voltaje_derecho):
    global x, y, angle
    velocidad_promedio = (voltaje_izquierdo + voltaje_derecho) / 2

    if voltaje_izquierdo == voltaje_derecho:
        dx = velocidad_promedio * math.cos(math.radians(angle))
        dy = -velocidad_promedio * math.sin(math.radians(angle))
        
        if (0 <= x + dx - largo // 2 and x + dx + largo // 2 <= WIDTH):
            x += dx
        if (0 <= y + dy - ancho // 2 and y + dy + ancho // 2 <= HEIGHT):
            y += dy
    else:
        angle_cambio = (voltaje_derecho - voltaje_izquierdo) / 20
        angle += angle_cambio
        dx = velocidad_promedio * math.cos(math.radians(angle))
        dy = -velocidad_promedio * math.sin(math.radians(angle))
        
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

# Función para dibujar el rastro del carrito
def dibujar_rastro():
    if len(rastro) > 1:
        pygame.draw.lines(window, RED, False, rastro, 2)

# Función para generar obstáculos
def generar_obstaculos(cantidad, tamaño):
    global obstaculos
    obstaculos.clear()  # Limpiar obstáculos anteriores
    for _ in range(cantidad):
        # Generar posiciones aleatorias dentro de los límites de la ventana
        ox = random.randint(tamaño // 2, WIDTH - tamaño // 2)
        oy = random.randint(tamaño // 2, HEIGHT - tamaño // 2)
        obstaculos.append((ox, oy))

# Función para dibujar los obstáculos en la pantalla
def dibujar_obstaculos():
    for obstaculo in obstaculos:
        pygame.draw.rect(window, BLUE, (obstaculo[0] - 20, obstaculo[1] - 20, 40, 40))

# Función para verificar colisiones
def verificar_colision():
    carrito_rect = pygame.Rect(x - largo // 2, y - ancho // 2, largo, ancho)  # Crear rectángulo del carrito
    for obstaculo in obstaculos:
        obstaculo_rect = pygame.Rect(obstaculo[0] - 20, obstaculo[1] - 20, 40, 40)  # Crear rectángulo del obstáculo
        if carrito_rect.colliderect(obstaculo_rect):  # Verificar colisión
            return True
    return False

# Generador para mover el carrito en espiral cuadrado
def mover_en_espiral(velocidad, incremento):
    global x, y, angle
    step_size = 10  # Tamaño del paso inicial
    direccion = 0  # 0: derecha, 1: abajo, 2: izquierda, 3: arriba

    while True:
        for _ in range(2):  # Dos repeticiones para cada distancia
            for _ in range(step_size):
                if verificar_colision():  # Verificar colisión antes de mover
                    return  # Detener si hay colisión

                if 0 < x < WIDTH and 0 < y < HEIGHT:  # Asegurarnos de que el carrito esté dentro de los límites
                    rastro.append((x, y))  # Solo se añade al rastro aquí
                else:
                    return  # Terminar si se sale de los límites

                if direccion == 0:  # Mover a la derecha
                    x += velocidad
                elif direccion == 1:  # Mover hacia abajo
                    y += velocidad
                elif direccion == 2:  # Mover hacia la izquierda
                    x -= velocidad
                else:  # Mover hacia arriba
                    y -= velocidad

                angle = {0: 0, 1: 90, 2: 180, 3: 270}[direccion]
                yield

            direccion = (direccion + 1) % 4  # Cambiar dirección

        step_size += incremento  # Aumentar el tamaño del paso

# Bucle principal del juego
clock = pygame.time.Clock()
running = True
espiral_gen = None
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
                angle = 90  # Reiniciar hacia el norte
                voltaje_izq_input.set_text('')
                voltaje_der_input.set_text('')
                poligono_vertices = []
                vertice_actual = 0
                rastro.clear()  # Limpiar el rastro
                espiral_gen = None  # Reiniciar espiral
                obstaculos.clear()  # Limpiar obstáculos

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == espiral_button:
                espiral_gen = mover_en_espiral(4,4)  # Iniciar el generador de espiral

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == obstaculos_button:
                generar_obstaculos(2, 40)  # Generar 5 obstáculos de 40x40 píxeles

            if event.user_type == pygame_gui.UI_DROP_DOWN_MENU_CHANGED and event.ui_element == dropdown_menu:
                figure_selected = event.text
                if figure_selected != 'Selecciona una figura':
                    if figure_selected == 'Círculo':
                        poligono_vertices = calcular_poligono(100, 100)
                    else:
                        lados = {
                            'Triángulo': 3,
                            'Cuadrado': 4,
                            'Pentágono': 5,
                            'Hexágono': 6,
                            'Heptágono': 7,
                            'Octágono': 8,
                            'Decágono': 10,
                            'Dodecágono': 12
                        }.get(figure_selected, 4)
                        poligono_vertices = calcular_poligono(lados, 100)
                    vertice_actual = 0

    if poligono_vertices:
        destino_x, destino_y = poligono_vertices[vertice_actual]
        if mover_carrito_a_punto(destino_x, destino_y, 2):
            vertice_actual = (vertice_actual + 1) % len(poligono_vertices)

        for i in range(len(poligono_vertices)):
            pygame.draw.line(window, BLUE, poligono_vertices[i], poligono_vertices[(i + 1) % len(poligono_vertices)], 2)

    if espiral_gen is not None:
        try:
            next(espiral_gen)  # Avanzar el generador de espiral
        except StopIteration:
            espiral_gen = None  # Finalizar el espiral cuando se complete

    # Verificar colisiones antes de mover el carrito
    if not verificar_colision():
        mover_carrito(voltaje_izquierdo, voltaje_derecho)  # El carrito se mueve pero no deja rastro

    dibujar_rastro()  # Dibujar el rastro en la pantalla
    dibujar_carrito()  # Dibujar el carrito
    dibujar_obstaculos()  # Dibujar obstáculos en la pantalla
    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.flip()

pygame.quit()