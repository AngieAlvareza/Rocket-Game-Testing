import pygame
import random
import os

# Inicialización de Pygame y del mezclador de sonido
pygame.init()
pygame.mixer.init()

# Carga y reproduce la música de fondo
pygame.mixer.music.load('musica.mp3')
pygame.mixer.music.play(-1)  # El argumento -1 hace que la música se reproduzca en bucle

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Shooter")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

font = pygame.font.Font(None, 36)

# Inicialización de puntuación, nivel y vidas
score = 0
level = 1
lives = 3  # Inicialización de vidas
watermelon_speed = 5

# Carga las imágenes de fondo
menu_background = pygame.image.load('menu_background2.webp')
menu_background = pygame.transform.scale(menu_background, (width, height))
game_background = pygame.image.load('background3.gif')
game_background = pygame.transform.scale(game_background, (width, height))

# Variables para el fondo en movimiento
bg_y1 = 0
bg_y2 = -height
bg_speed = 1

def draw_text(text, color, x, y, font_size=36):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

def load_best_score():
    # Cargar el mejor puntaje desde un archivo (puedes implementar esto basado en tu lógica de almacenamiento)
    best_score = 0
    best_player = "No one"
    try:
        with open('best_score.txt', 'r') as file:
            for line in file:
                player, score_str = line.strip().split(':')
                player_score = int(score_str)
                if player_score > best_score:
                    best_score = player_score
                    best_player = player
    except FileNotFoundError:
        pass  # Maneja el caso cuando el archivo no existe

    return best_player, best_score

def save_best_score(player, score):
    # Guardar el nuevo mejor puntaje en el archivo
    with open('best_score.txt', 'w') as file:
        file.write(f'{player}: {score}\n')

def main_menu():
    best_player, best_score = load_best_score()

    menu = True
    while menu:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        # Dibuja la imagen de fondo del menú
        screen.blit(menu_background, (0, 0))

        # Mostrar el mejor puntaje y el jugador
        draw_text(f"Mejor Puntaje: {best_score} - {best_player}", WHITE, width // 2 - 200, 50)

        pygame.display.update()
        pygame.time.Clock().tick(15)

def pause_menu():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:  # Continuar
                    paused = False
                elif event.key == pygame.K_q:  # Salir
                    pygame.quit()
                    quit()

        screen.fill(BLACK)
        draw_text('Juego Pausado', GREEN, width // 2 - 100, height // 2 - 100)
        draw_text('Presiona C para continuar', WHITE, width // 2 - 160, height // 2)
        draw_text('Presiona Q para salir', RED, width // 2 - 130, height // 2 + 50)
        pygame.display.update()
        pygame.time.Clock().tick(5)

class Rocket:
    def __init__(self):
        self.frames = [pygame.image.load(os.path.join("cohete_frames", f)) for f in os.listdir("cohete_frames") if f.endswith(".gif")]
        self.current_frame = 0
        self.image = pygame.transform.scale(self.frames[self.current_frame], (50, 100))
        self.rect = self.image.get_rect(center=(width // 2, height - 30))
        self.speed = 7
        self.level = 1
        self.frame_delay = 5
        self.frame_count = 0

    def draw(self):
        self.frame_count += 1
        if self.frame_count >= self.frame_delay:
            self.frame_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.current_frame], (50, 100))
        screen.blit(self.image, self.rect)
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < width:
            self.rect.x += self.speed

    def evolve(self):
        self.level += 1
        # Se podría cambiar la imagen o agregar otras mejoras visuales y funcionales aquí

class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def update(self):
        self.rect.y += self.speed

class Watermelon:
    def __init__(self):
        # Selecciona la imagen basada en el nivel actual
        if level == 1:
            self.original_image = pygame.image.load("watermelon.png")  # Sandía para el nivel 1
        elif level == 2:
            self.original_image = pygame.image.load("chirimoya.png")   # Chirimoya para el nivel 2
        elif level == 3:
            self.original_image = pygame.image.load("manzana.png")       # Manzana para el nivel 3
        elif level == 4:
            self.original_image = pygame.image.load("banana.png")      # Banana para el nivel 4
        self.image = pygame.transform.scale(self.original_image, (50, 50))
        self.rect = self.image.get_rect(center=(random.randint(20, width-20), 0))
        self.speed = watermelon_speed

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += self.speed




def check_level_up():
    global level, score, watermelon_speed
    if score >= level * 100:
        level += 1
        watermelon_speed += 2
        for watermelon in watermelons:  # Actualizar la velocidad de las sandías existentes
            watermelon.speed = watermelon_speed
        if level % 10 == 0:
            rocket.evolve()  # Evolucionar el cohete cada 10 niveles

def game_over():
    global score, lives

    # Pausar la música de fondo
    pygame.mixer.music.pause()

    # Mostrar pantalla de Game Over y obtener el nombre del jugador
    input_rect = pygame.Rect(width // 2 - 150, height // 2 - 50, 300, 40)
    name = ""
    active = True
    while active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    active = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
        
        screen.fill(BLACK)
        # Mostrar '¡Game Over!' centrado en la parte superior de la pantalla
        draw_text('-----¡Game Over!-----', RED, width // 2 - 100, height // 2 - 150)
        
        # Mostrar 'Ingresa tu nombre:' debajo de '¡Game Over!'
        draw_text('Ingresa tu nombre:', WHITE, width // 2 - 100, height // 2 - 100)
        
        # Dibujar la caja de entrada para el nombre y su borde blanco
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        
        # Mostrar 'Ingresa tu nombre' centrado en la caja de entrada
        draw_text('', WHITE, input_rect.x + input_rect.width // 2, input_rect.y + input_rect.height // 2 - 10)
        
        pygame.draw.rect(screen, WHITE, input_rect, 2)
        draw_text(name, WHITE, input_rect.x + 5, input_rect.y + 5)
        pygame.display.flip()
        pygame.time.Clock().tick(30)

    # Guardar nombre y puntuación en un archivo
    with open('scores.txt', 'a') as file:
        file.write(f'{name}: {score}\n')

    # Guardar el nuevo mejor puntaje si corresponde
    best_player, best_score = load_best_score()
    if score > best_score:
        save_best_score(name, score)

    # Mostrar el nombre y la puntuación obtenida
    draw_text(f'Tu puntuación: {score}', WHITE, width // 2 - 100, height // 2 + 50, font_size=36)


    pygame.display.flip()
    pygame.time.delay(2000)  # Esperar 2 segundos antes de mostrar el menú principal

    # Reiniciar valores para un nuevo juego
    score = 0
    level = 1
    lives = 3
    pygame.mixer.music.unpause()
    main_menu()

main_menu()

rocket = Rocket()
projectiles = []
watermelons = []
watermelon_event = pygame.USEREVENT + 1
pygame.time.set_timer(watermelon_event, 2000)

# Cargar el sonido de pistola
gunshot_sound = pygame.mixer.Sound('pistola.mp3')

# Cargar el sonido de choque
collision_sound = pygame.mixer.Sound('choque.mp3')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(rocket.rect.centerx, rocket.rect.top))
                gunshot_sound.play()  # Reproducir el sonido de pistola al disparar
            if event.key == pygame.K_p:
                pause_menu()
        if event.type == watermelon_event:
            watermelons.append(Watermelon())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket.move("left")
    if keys[pygame.K_RIGHT]:
        rocket.move("right")

    # Mover el fondo
    bg_y1 += bg_speed
    bg_y2 += bg_speed
    if bg_y1 >= height:
        bg_y1 = -height
    if bg_y2 >= height:
        bg_y2 = -height

    # Dibujar fondo del juego
    screen.blit(game_background, (0, bg_y1))
    screen.blit(game_background, (0, bg_y2))

    rocket.draw()
    for projectile in projectiles[:]:
        projectile.update()
        projectile.draw()
        if projectile.rect.bottom < 0:
            projectiles.remove(projectile)

    # Lista temporal para las sandías que se van a eliminar
    watermelons_to_remove = []

    for watermelon in watermelons[:]:
        watermelon.update()
        watermelon.draw()
        if watermelon.rect.top > height:
            watermelons_to_remove.append(watermelon)
            score -= 5  # Resta 5 puntos si una sandía no es eliminada
            if score < 0:
                score = 0  # Asegura que la puntuación no sea negativa
        if rocket.rect.colliderect(watermelon.rect):
            watermelons_to_remove.append(watermelon)
            lives -= 1  # Resta una vida si el cohete choca con una sandía
            collision_sound.play()  # Reproducir el sonido de choque
            if lives < 0:
                lives = 0  # Asegura que las vidas no sean negativas
        for projectile in projectiles[:]:
            if projectile.rect.colliderect(watermelon.rect):
                projectiles.remove(projectile)
                watermelons_to_remove.append(watermelon)
                score += 10
                check_level_up()

    # Eliminar todas las sandías que deben ser eliminadas
    for watermelon in watermelons_to_remove:
        if watermelon in watermelons:
            watermelons.remove(watermelon)

    # Verificar si el juego ha terminado
    if lives <= 0:
        game_over()

    # Dibujar vidas restantes
    draw_text(f'Vidas: {lives}', WHITE, 10, height - 40)

    draw_text(f'Nivel: {level}', WHITE, 10, 30)
    draw_text(f'Score: {score}', WHITE, width - 150, 30)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
