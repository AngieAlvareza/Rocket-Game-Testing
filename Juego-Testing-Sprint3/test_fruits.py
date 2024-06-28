import pytest
from unittest.mock import patch
from cohete import Rocket, Watermelon, level
import pygame

# Configuración de Pygame para pruebas
pygame.init()
pygame.mixer.init()

@pytest.fixture
def setup_level():
    global level
    level = 1

@pytest.fixture
def watermelon():
    return Watermelon()

# Caso de Prueba: Verificar que la fruta es una sandía en el nivel 1
def test_fruit_level_1(watermelon, setup_level):
    global level
    level = 1
    watermelon = Watermelon()
    assert watermelon.original_image.get_at((0, 0)) == pygame.image.load("watermelon.png").get_at((0, 0)), "La fruta no es una sandía en el nivel 1"

# Caso de Prueba: Verificar que la fruta es una chirimoya en el nivel 2
def test_fruit_level_2(watermelon):
    global level
    level = 2
    watermelon = Watermelon()
    assert watermelon.original_image.get_at((0, 0)) == pygame.image.load("chirimoya.png").get_at((0, 0)), "La fruta no es una chirimoya en el nivel 2"



if __name__ == "__main__":
    pytest.main()
