import pytest
from unittest.mock import patch, MagicMock
import pygame

# Inicialización de Pygame para pruebas
pygame.init()
pygame.mixer.init()

@pytest.fixture
def setup_music():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)

# Caso de Prueba: Verificar que la música se carga correctamente
def test_load_music():
    try:
        pygame.mixer.music.load('musica.mp3')
    except pygame.error:
        pytest.fail("Error al cargar el archivo de música")

# Caso de Prueba: Verificar que la música se reproduce en bucle
def test_play_music_loop(setup_music):
    assert pygame.mixer.music.get_busy() == True

# Caso de Prueba: Pausar y reanudar la música
def test_pause_resume_music(setup_music):
    pygame.mixer.music.pause()
    assert pygame.mixer.music.get_busy() == False
    pygame.mixer.music.unpause()
    assert pygame.mixer.music.get_busy() == True

# Caso de Prueba: Detener la música
def test_stop_music(setup_music):
    pygame.mixer.music.stop()
    assert pygame.mixer.music.get_busy() == False

# Caso de Prueba: Ajustar el volumen de la música
def test_music_volume(setup_music):
    pygame.mixer.music.set_volume(0.5)
    assert pygame.mixer.music.get_volume() == 0.5





# Caso de Prueba: Verificar que la música se reanuda después de pausar
def test_music_resume_after_pause(setup_music):
    pygame.mixer.music.pause()
    pygame.mixer.music.unpause()
    assert pygame.mixer.music.get_busy() == True

# Caso de Prueba: Verificar que la música se detiene al terminar el juego
def test_music_stop_on_game_over(setup_music):
    pygame.mixer.music.stop()
    assert pygame.mixer.music.get_busy() == False

# Caso de Prueba: Verificar que la música se reanuda al reiniciar el juego
def test_music_resume_on_game_restart(setup_music):
    pygame.mixer.music.stop()
    pygame.mixer.music.play(-1)
    assert pygame.mixer.music.get_busy() == True


if __name__ == "__main__":
    pytest.main()
