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

# Botón para agregar carritos
agregar_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 170), (150, 30)),
    text='Agregar Carros',
    manager=manager
)

# Lista de carritos
carritos = []

# Parámetros del carrito inicial
x, y = WIDTH // 2, HEIGHT // 2
angle = 90  # El carrito inicialmente apunta hacia el norte (90 grados)
largo = 50
ancho = 30
tamaño_rueda = 8

# Clase Carrito
class Carrito:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle
        self.voltaje_izquierdo = 0
        self.voltaje_derecho = 0
        self.largo = 50
        self.ancho = 30
        self.carrito_surface = pygame.Surface((self.largo, self.ancho))
        self.carrito_surface.fill(RED)
        self.carrito_surface.set_colorkey(WHITE)

    def mover(self):
        velocidad_promedio = (self.voltaje_izquierdo + self.voltaje_derecho) / 2

        if self.voltaje_izquierdo == self.voltaje_derecho:
            dx = velocidad_promedio * math.cos(math.radians(self.angle))
            dy = -velocidad_promedio * math.sin(math.radians(self.angle))

            if 0 <= self.x + dx - self.largo // 2 and self.x + dx + self.largo // 2 <= WIDTH:
                self.x += dx
            if 0 <= self.y + dy - self.ancho // 2 and self.y + dy + self.ancho // 2 <= HEIGHT:
                self.y += dy
        else:
            angle_cambio = (self.voltaje_derecho - self.voltaje_izquierdo) / 20
            self.angle += angle_cambio

    def dibujar(self, window):
        # Dibuja el cuerpo del carrito
        rotated_surface = pygame.transform.rotate(self.carrito_surface, self.angle)
        new_rect = rotated_surface.get_rect(center=(self.x, self.y))
        window.blit(rotated_surface, new_rect.topleft)
        
        # Mantener las llantas como antes (cuadritos grises)
        distancia_ruedas = self.largo // 2 - 5
        rueda_izq_x = self.x - distancia_ruedas * math.sin(math.radians(self.angle))
        rueda_izq_y = self.y - distancia_ruedas * math.cos(math.radians(self.angle))
        rueda_der_x = self.x + distancia_ruedas * math.sin(math.radians(self.angle))
        rueda_der_y = self.y + distancia_ruedas * math.cos(math.radians(self.angle))
        
        pygame.draw.rect(window, GRAY, (rueda_izq_x - tamaño_rueda // 2, rueda_izq_y - tamaño_rueda // 2, tamaño_rueda, tamaño_rueda))
        pygame.draw.rect(window, GRAY, (rueda_der_x - tamaño_rueda // 2, rueda_der_y - tamaño_rueda // 2, tamaño_rueda, tamaño_rueda))

# Función para agregar carritos a los lados de todos los carritos existentes
def agregar_carritos_lados():
    # Agregar carritos a los lados de cada carrito existente
    nuevos_carritos = []
    for carrito in carritos:
        # Calcular las posiciones a la izquierda y derecha del carrito actual
        distancia = 65  # Distancia entre carritos

        # Carrito a la izquierda
        nuevo_x_izq = carrito.x - distancia
        nuevo_y_izq = carrito.y
        carrito_izquierdo = Carrito(nuevo_x_izq, nuevo_y_izq, 90)
        nuevos_carritos.append(carrito_izquierdo)

        # Carrito a la derecha
        nuevo_x_der = carrito.x + distancia
        nuevo_y_der = carrito.y
        carrito_derecho = Carrito(nuevo_x_der, nuevo_y_der, 90)
        nuevos_carritos.append(carrito_derecho)

    # Agregar los nuevos carritos a la lista
    carritos.extend(nuevos_carritos)

    print(f"Carros agregados: {len(carritos)}")  # Para depurar cuántos carros se agregan

# Mostrar advertencia
def mostrar_advertencia(mensaje):
    pygame_gui.windows.UIMessageWindow(
        rect=pygame.Rect((200, 150), (400, 200)),
        manager=manager,
        window_title="Advertencia",
        html_message=mensaje
    )

# Agregar el carrito principal al inicio
carritos.append(Carrito(x, y, angle))

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

                    # Aplicar voltajes a todos los carritos
                    for carrito in carritos:
                        carrito.voltaje_izquierdo = voltaje_izquierdo
                        carrito.voltaje_derecho = voltaje_derecho

                    # Verificar si están dentro del rango permitido
                    if not -15 <= voltaje_izquierdo <= 15 or not -15 <= voltaje_derecho <= 15:
                        mostrar_advertencia("Voltajes fuera de rango. Deben estar entre -15 y 15.")
                        for carrito in carritos:
                            carrito.voltaje_izquierdo, carrito.voltaje_derecho = 0, 0

                except ValueError:
                    mostrar_advertencia("Entrada inválida. Ingrese solo números.")

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == reset_button:
                voltaje_izquierdo = 0
                voltaje_derecho = 0
                carritos.clear()  # Reiniciar la lista de carritos
                carritos.append(Carrito(x, y, angle))  # Volver a agregar el carrito principal
                voltaje_izq_input.set_text('')
                voltaje_der_input.set_text('')

            if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == agregar_button:
                agregar_carritos_lados()  # Agregar carritos a los lados del carrito principal

    # Mover y dibujar cada carrito
    for carrito in carritos:
        carrito.mover()
        carrito.dibujar(window)

    manager.update(time_delta)
    manager.draw_ui(window)
    pygame.display.flip()

pygame.quit()
