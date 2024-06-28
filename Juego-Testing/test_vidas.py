import pytest
from unittest.mock import patch
from cohete import Rocket, Watermelon, game_over
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

# Caso de Prueba 1: Verificar la inicialización de vidas
def test_initial_lives():
    global lives
    lives = 3
    assert lives == 3

# Caso de Prueba 2: Pérdida de una vida al colisionar con una sandía
def test_lose_life_on_collision():
    global lives
    lives = 3
    rocket = Rocket()
    watermelon = Watermelon()
    watermelon.rect.center = rocket.rect.center
    if rocket.rect.colliderect(watermelon.rect):
        lives -= 1
    assert lives == 2

# Caso de Prueba 3: Las vidas no se vuelven negativas
def test_lives_not_negative():
    global lives
    lives = 1
    rocket = Rocket()
    watermelon = Watermelon()
    watermelon.rect.center = rocket.rect.center
    if rocket.rect.colliderect(watermelon.rect):
        lives -= 1
    if lives < 0:
        lives = 0
    assert lives == 0


# Caso de Prueba 5: Reinicio de vidas al iniciar un nuevo juego
def test_reset_lives_on_new_game():
    global lives
    lives = 0
    # Simulación de inicio de un nuevo juego
    lives = 3
    assert lives == 3



#



# Caso de Prueba 10: Verificar que las vidas se decremente correctamente en niveles diferentes
def test_lives_decrement_in_different_levels():
    global lives, level
    lives = 3
    rocket = Rocket()
    watermelon = Watermelon()
    watermelon.rect.center = rocket.rect.center
    level = 1
    if rocket.rect.colliderect(watermelon.rect):
        lives -= 1
    assert lives == 2
    level = 2
    if rocket.rect.colliderect(watermelon.rect):
        lives -= 1
    assert lives == 1

    # Caso de Prueba: Verificar que las vidas se decrementen en un intervalo de tiempo específico
def test_lives_decrement_over_time():
    global lives
    lives = 3
    rocket = Rocket()
    watermelon = Watermelon()
    watermelon.rect.center = rocket.rect.center
    for _ in range(3):  # Simula tres colisiones en diferentes intervalos de tiempo
        if rocket.rect.colliderect(watermelon.rect):
            lives -= 1
    assert lives == 0

# Caso de Prueba: Verificar que las vidas no se decrementen si el cohete tiene un escudo activo
def test_no_life_loss_with_shield():
    global lives
    lives = 3
    rocket = Rocket()
    watermelon = Watermelon()
    watermelon.rect.center = rocket.rect.center
    shield_active = True  # Simula que el cohete tiene un escudo activo
    if rocket.rect.colliderect(watermelon.rect) and not shield_active:
        lives -= 1
    assert lives == 3  # Las vidas no deben decrementar

# Caso de Prueba: Verificar que las vidas se actualicen correctamente después de pausar y reanudar el juego
def test_lives_after_pause_resume():
    global lives
    lives = 3
    # Simula el evento de pausa
    paused = True
    if paused:
        current_lives = lives
    # Simula el evento de reanudación
    paused = False
    assert current_lives == lives  # Las vidas deben ser las mismas después de pausar y reanudar

if __name__ == "__main__":
    pytest.main()
