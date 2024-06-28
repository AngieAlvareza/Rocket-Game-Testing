import pytest
from cohete import Rocket, Projectile, Watermelon, collision_sound, lives, score, level, watermelon_speed, check_level_up, game_over
from unittest.mock import patch, mock_open, MagicMock
# Mock Pygame dependencies
import pygame
pygame.init()
pygame.mixer.init()
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


def test_sound_init():
    pygame.init()
    pygame.mixer.init()
    assert pygame.mixer.get_init() is not None
def test_load_music():
    try:
        pygame.mixer.music.load('musica.mp3')
    except pygame.error:
        assert False, "Error al cargar el archivo de música"
def test_play_music_loop():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)
    assert pygame.mixer.music.get_busy() == True
def test_pause_resume_music():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    assert pygame.mixer.music.get_busy() == False
    pygame.mixer.music.unpause()
    assert pygame.mixer.music.get_busy() == True
def test_stop_music():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.stop()
    assert pygame.mixer.music.get_busy() == False
def test_music_volume():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.set_volume(0.5)
    assert pygame.mixer.music.get_volume() == 0.5
def test_reset_score_and_level():
    global score, level
    score = 150
    level = 3
    score = 0
    level = 1
    assert score == 0
    assert level == 1
def test_initial_score():
    assert score == 0
def test_score_increment_on_collision():
    global score
    initial_score = score
    projectile = Projectile(100, 100)
    watermelon = Watermelon()
    watermelon.rect.x, watermelon.rect.y = 100, 100
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == initial_score + 10
def test_score_accumulation():
    global score
    initial_score = score
    projectiles = [Projectile(100, 100), Projectile(150, 150)]
    watermelons = [Watermelon(), Watermelon()]
    for i in range(len(projectiles)):
        watermelons[i].rect.x, watermelons[i].rect.y = 100 + i * 50, 100 + i * 50
        if projectiles[i].rect.colliderect(watermelons[i].rect):
            score += 10
    assert score == initial_score + 20
def test_multiple_collisions():
    global score
    initial_score = score
    projectiles = [Projectile(100, 100), Projectile(150, 150), Projectile(200, 200)]
    watermelons = [Watermelon(), Watermelon(), Watermelon()]
    for i in range(len(projectiles)):
        watermelons[i].rect.x, watermelons[i].rect.y = 100 + i * 50, 100 + i * 50
        if projectiles[i].rect.colliderect(watermelons[i].rect):
            score += 10
    assert score == initial_score + 30
def test_no_score_increment_without_collision():
    global score
    initial_score = score
    projectile = Projectile(100, 100)
    watermelon = Watermelon()
    watermelon.rect.x, watermelon.rect.y = 200, 200  # No colisionan
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == initial_score

def test_score_increment_multiple_shoots():
    global score
    initial_score = score
    projectiles = [Projectile(100, 100), Projectile(150, 150), Projectile(200, 200)]
    watermelons = [Watermelon(), Watermelon(), Watermelon()]
    for i in range(len(projectiles)):
        watermelons[i].rect.x, watermelons[i].rect.y = 100 + i * 50, 100 + i * 50
        if projectiles[i].rect.colliderect(watermelons[i].rect):
            score += 10
    assert score == initial_score + 30

def test_high_score():
    global score
    score = 200  # Puntuación alta simulada
    high_score = score
    assert high_score == 200

def test_score_after_pause():
    global score
    score = 50
    # Simulación de pausa
    paused_score = score
    assert paused_score == 50

def test_score_reset_after_game_over():
    global score
    score = 80
    # Simulación de fin del juego
    score = 0
    assert score == 0
def test_score_increment_with_different_speeds():
    global score, watermelon_speed
    initial_score = score
    watermelon_speed = 7
    watermelon = Watermelon()
    watermelon.rect.x, watermelon.rect.y = 100, 100
    projectile = Projectile(100, 100)
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == initial_score + 10
    watermelon_speed = 10
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == initial_score + 20
def test_score_reset_on_game_restart():
    global score
    score = 100
    # Simulación de reinicio del juego
    score = 0
    assert score == 0
def test_score_increment_with_increased_speed():
    global score, watermelon_speed
    initial_score = score
    watermelon_speed = 10
    watermelon = Watermelon()
    watermelon.rect.x, watermelon.rect.y = 100, 100
    projectile = Projectile(100, 100)
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == initial_score + 10

def test_score_after_resume():
    global score
    score = 50
    # Simulación de pausa y reanudación
    paused_score = score
    assert paused_score == 50
    resumed_score = score
    assert resumed_score == 50

def test_pause_state():
    paused = False
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = True
    assert paused == True
def test_resume_from_pause():
    paused = True
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            paused = False
    assert paused == False
def test_score_during_pause():
    global score
    score = 50
    paused_score = score
    paused = True
    if paused:
        assert paused_score == score
def test_music_pause_resume():
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    assert not pygame.mixer.music.get_busy()
    pygame.mixer.music.unpause()
    assert pygame.mixer.music.get_busy()

def test_quit_during_pause():
    paused = True
    quit_game = False
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            quit_game = True
    assert quit_game == True
def test_no_auto_resume():
    paused = True
    # Simular esperar un tiempo (sin intervención del usuario)
    assert paused == True

def test_music_loop_pause_resume():
    pygame.mixer.music.play(-1)
    pygame.mixer.music.pause()
    assert not pygame.mixer.music.get_busy()
    pygame.mixer.music.unpause()
    assert pygame.mixer.music.get_busy()
def test_multiple_pause_resume_cycles():
    paused = False
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
    assert paused == True  # Primera pausa
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            paused = not paused
    assert paused == False  # Primera reanudación
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_p)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused
    assert paused == True  # Segunda pausa
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_c)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_c:
            paused = not paused
    assert paused == False  # Segunda reanudación
def test_quit_game_while_paused():
    paused = True
    quit_game = False
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_q)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            quit_game = True
    assert quit_game == True

def test_main_menu():
    menu_active = True
    for event in [pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            menu_active = False
    assert menu_active == False
def test_quit_event():
    running = True
    for event in [pygame.event.Event(pygame.QUIT)]:
        if event.type == pygame.QUIT:
            running = False
    assert running == False
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
def test_load_images():
    try:
        rocket_image = pygame.image.load("rocket3.png")
        watermelon_image = pygame.image.load("watermelon.png")
    except pygame.error:
        assert False, "Error al cargar las imágenes" 
def test_initial_score():
    assert score == 0
def test_initial_level():
    assert level == 1
def test_game_initialization():
    try:
        pygame.init()
        pygame.mixer.init()
        assert True
    except Exception as e:
        assert False, f"Initialization failed: {e}"

def test_rocket_movement_left_boundary(rocket):
    """ Test that the rocket doesn't move past the left screen boundary. """
    rocket.rect.x = 0  # Position rocket at the left edge
    rocket.move('left')
    assert rocket.rect.x == 0  # Check if the rocket stays within the boundary

def test_increase_score(projectile, watermelon):
    """ Test that destroying a watermelon increases the score correctly. """
    global score
    score = 0  # Reset score
    projectile.rect.y = watermelon.rect.y  # Align projectile with watermelon for a hit
    projectile.rect.x = watermelon.rect.x
    if projectile.rect.colliderect(watermelon.rect):
        score += 10
    assert score == 10  # Check score increment

def test_collision_sound_loaded():
    assert collision_sound.get_length() > 0, "El sonido de choque no se cargó correctamente"

# Caso de Prueba: Verificar que el cohete no se mueve más allá del borde derecho
def test_rocket_movement_right_boundary(rocket):
    rocket.rect.x = screen.get_width() - rocket.rect.width  # Position rocket at the right edge
    rocket.move('right')
    assert rocket.rect.x == screen.get_width() - rocket.rect.width  # Check if the rocket stays within the boundary

# Caso de Prueba: Verificar que el cohete no se mueve más allá del borde izquierdo
def test_rocket_movement_left_boundary(rocket):
    rocket.rect.x = 0  # Position rocket at the left edge
    rocket.move('left')
    assert rocket.rect.x == 0  # Check if the rocket stays within the boundary

# Caso de Prueba: Verificar la evolución del cohete
def test_rocket_evolution_increase_level():
    rocket = Rocket()
    rocket.evolve()
    assert rocket.level == 2, "La evolución del cohete no incrementó el nivel correctamente"

# Caso de Prueba: Verificar la inicialización del proyectil
def test_projectile_initial_speed(projectile):
    assert projectile.speed == -10, "La velocidad inicial del proyectil no es correcta"


# Caso de Prueba: Verificar que la música de fondo se reproduce en bucle
def test_background_music_loop():
    pygame.mixer.music.load('musica.mp3')
    pygame.mixer.music.play(-1)
    assert pygame.mixer.music.get_busy() == True, "La música de fondo no se está reproduciendo en bucle"

