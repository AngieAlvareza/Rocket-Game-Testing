import pytest
from cohete import Rocket, Projectile, Watermelon

# Mock Pygame dependencies
import pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

@pytest.fixture
def rocket():
    return Rocket()

@pytest.fixture
def projectile():
    return Projectile(100, 100)

@pytest.fixture
def watermelon():
    return Watermelon()

def test_rocket_initial_position(rocket):
    assert rocket.rect.centerx == 400
    assert rocket.rect.centery == 570

def test_rocket_move_left(rocket):
    initial_x = rocket.rect.x
    rocket.move("left")
    assert rocket.rect.x < initial_x

def test_rocket_move_right(rocket):
    initial_x = rocket.rect.x
    rocket.move("right")
    assert rocket.rect.x > initial_x

def test_projectile_initial_position(projectile):
    assert projectile.rect.x == 100
    assert projectile.rect.y == 100

def test_projectile_update(projectile):
    initial_y = projectile.rect.y
    projectile.update()
    assert projectile.rect.y < initial_y

def test_watermelon_initial_position(watermelon):
    assert 20 <= watermelon.rect.centerx <= 780
    assert watermelon.rect.centery == 0

def test_watermelon_update(watermelon):
    initial_y = watermelon.rect.y
    watermelon.update()
    assert watermelon.rect.y > initial_y
