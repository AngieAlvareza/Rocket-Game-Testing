class Projectile:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 10)
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
