import pytest
from unittest.mock import patch
from cohete import Rocket, Watermelon, collision_sound
import pygame

# Configuración de Pygame para pruebas
pygame.init()
pygame.mixer.init()

@pytest.fixture
def rocket():
    return Rocket()

@pytest.fixture
def watermelon():
    return Watermelon()

if __name__ == "__main__":
    pytest.main()
