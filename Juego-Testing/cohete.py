import pygame
import random
import pygame.mixer

# Inicialización de Pygame
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

# Inicialización de puntuación y nivel
score = 0
level = 1
watermelon_speed = 5

# Carga las imágenes de fondo
menu_background = pygame.image.load('menu_background3.webp')
menu_background = pygame.transform.scale(menu_background, (width, height))
game_background = pygame.image.load('background2.jpg')
game_background = pygame.transform.scale(game_background, (width, height))

def draw_text(text, color, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    screen.blit(textobj, textrect)

def main_menu():
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
        self.original_image = pygame.image.load("rocket3.png")
        self.image = pygame.transform.scale(self.original_image, (50, 100))
        self.rect = self.image.get_rect(center=(width // 2, height - 30))
        self.speed = 7

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < width:
            self.rect.x += self.speed

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
        self.original_image = pygame.image.load("watermelon.png")
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

main_menu()

rocket = Rocket()
projectiles = []
watermelons = []
watermelon_event = pygame.USEREVENT + 1
pygame.time.set_timer(watermelon_event, 2000)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(rocket.rect.centerx, rocket.rect.top))
            if event.key == pygame.K_p:
                pause_menu()
        if event.type == watermelon_event:
            watermelons.append(Watermelon())

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket.move("left")
    if keys[pygame.K_RIGHT]:
        rocket.move("right")

    # Dibujar fondo del juego
    screen.blit(game_background, (0, 0))

    rocket.draw()
    for projectile in projectiles[:]:
        projectile.update()
        projectile.draw()
        if projectile.rect.bottom < 0:
            projectiles.remove(projectile)
    for watermelon in watermelons[:]:
        watermelon.update()
        watermelon.draw()
        if watermelon.rect.top > height:
            watermelons.remove(watermelon)
        for projectile in projectiles[:]:
            if projectile.rect.colliderect(watermelon.rect):
                projectiles.remove(projectile)
                watermelons.remove(watermelon)
                score += 10
                check_level_up()
    draw_text(f'Nivel: {level}', WHITE, 10, 30)
    draw_text(f'Score: {score}', WHITE, width - 150, 30)
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
