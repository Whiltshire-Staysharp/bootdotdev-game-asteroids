import pygame
import sys
from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from highscore import load_high_scores, is_high_score, save_high_scores
from logger import log_state, log_event

def show_start_screen(screen, font):
    scores = load_high_scores()
    waiting = True

    while waiting:
        screen.fill("black")
        title = font.render("TOP 10 PILOTS", True, "white")
        screen.blit(title, (SCREEN_WIDTH // 2 - 100, 50))

        for i, entry in enumerate(scores):
            score_text = font.render(f"{i+1}. {entry['name']:8} - {entry['score']}", True, "green")
            screen.blit(score_text, (SCREEN_WIDTH // 2 - 150, 120 + (i * 40)))
            
        prompt = font.render("Press SPACE to Start", True, "yellow")
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100))
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def get_player_name(screen, font):
    name = ""
    entering = True
    while entering:
        screen.fill("black")
        prompt = font.render("NEW HIGH SCORE! ENTER NAME:", True, "cyan")
        # Add a flashing underscore for the cursor effect
        name_surface = font.render(name + "_", True, "white")
        
        screen.blit(prompt, (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 50))
        screen.blit(name_surface, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(name) > 0:
                        entering = False
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Only allow letters and numbers, max 8 chars
                    if len(name) < 8 and event.unicode.isalnum():
                        name += event.unicode.upper()
    return name

def main():
    pygame.init()

    version = pygame.version.ver
    print(f"Starting Asteroids with pygame version: {version}")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont("monospace", 35)

    # CALL THE START SCREEN HERE
    show_start_screen(screen, font)

    score = 0

	# Initialise the Clock and dt (delta time)
    clock = pygame.time.Clock()
    dt = 0

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable,)
    Shot.containers = (shots, updatable, drawable)

    # Instantiate the Player in the centre of the screen
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # The Game Loop
    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            pass

        # Update all objects in the updatable group
        for obj in updatable:
            obj.update(dt)

        for asteroid in asteroids:
            if asteroid.collides_with(player):
                log_event("player_hit")
                print("Game over!")

                if is_high_score(score):
                    name = get_player_name(screen, font)
                    current_scores = load_high_scores()
                    current_scores.append({"name": name, "score": score})
                    save_high_scores(current_scores)

                sys.exit()
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    points_earned = asteroid.split()
                    score += points_earned
                    shot.kill()

        screen.fill("black")
        # Draw the player to the screen

        # Basic score display
        font = pygame.font.SysFont("monospace", 35)
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_surface, (10, 10))

        for obj in drawable:
            obj.draw(screen)
        # flip() must happen After drawing everthing
        pygame.display.flip()
        
        # Limit the frame-rate to 60 FPS
        # .tick(60) returns the milliseconds passed since the last frame
        milliseconds = clock.tick(60)
        dt = milliseconds / 1000
        print(dt)

if __name__ == "__main__":
    main()