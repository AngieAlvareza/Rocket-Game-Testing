import pygame
import random

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rocket Shooter")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clase para el cohete
class Rocket:
    def __init__(self):
        self.original_image = pygame.image.load("rocket3.png")  # Carga la imagen original del cohete
        self.image = pygame.transform.scale(self.original_image, (50, 100))  # Redimensiona la imagen a 50x100 píxeles
        self.rect = self.image.get_rect(center=(width // 2, height - 30))
        self.speed = 7

    def draw(self):
        screen.blit(self.image, self.rect)
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        elif direction == "right" and self.rect.right < width:
            self.rect.x += self.speed

# Clase para los proyectiles
class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10

    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

    def update(self):
        self.rect.y += self.speed

# Clase para las sandías
class Watermelon:
    def __init__(self):
        self.original_image = pygame.image.load("watermelon.png")  # Carga la imagen original
        self.image = pygame.transform.scale(self.original_image, (50, 50))  # Redimensiona la imagen a 50x50 píxeles
        self.rect = self.image.get_rect(center=(random.randint(20, width-20), 0))

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect.y += 5


# Setup
rocket = Rocket()
projectiles = []
watermelons = []
watermelon_event = pygame.USEREVENT + 1
pygame.time.set_timer(watermelon_event, 2000)  # Genera una sandía cada 2 segundos

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(rocket.rect.centerx, rocket.rect.top))
        if event.type == watermelon_event:
            watermelons.append(Watermelon())

    # Control de entrada del usuario
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        rocket.move("left")
    if keys[pygame.K_RIGHT]:
        rocket.move("right")

    # Actualización de la pantalla
    screen.fill(BLACK)
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
                break

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
