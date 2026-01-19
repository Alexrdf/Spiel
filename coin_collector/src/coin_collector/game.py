import pygame
import sys
from .config import load_level

PLAYER_SIZE = 30
PLAYER_SPEED = 4

def rect_from_xywh(x, y, w, h) -> pygame.Rect:
    return pygame.Rect(int(x), int(y), int(w), int(h))

def run_game(level_path: str, fps: int = 60, debug: bool = False) -> None:
    lvl = load_level(level_path)

    pygame.init()
    screen = pygame.display.set_mode((lvl.width, lvl.height))
    pygame.display.set_caption("Coin Collector")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    # Initialisierung der Objekte
    player = pygame.Rect(lvl.player_start.x, lvl.player_start.y, PLAYER_SIZE, PLAYER_SIZE)
    coins = [pygame.Rect(c.x - c.r, c.y - c.r, c.r*2, c.r*2) for c in lvl.coins]
    walls = [rect_from_xywh(w.x, w.y, w.w, w.h) for w in lvl.walls]
    
    score = 0
    total_coins = len(coins)
    running = True

    while running:
        clock.tick(fps)
        
        # 1. Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_F12:
                    pygame.image.save(screen, "screenshot.png")

        # 2. Bewegung & Steuerung
        keys = pygame.key.get_pressed()
        vx = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        vy = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])

        if vx != 0 and vy != 0:
            vx *= 0.7071
            vy *= 0.7071

        # X-Kollision
        player.x += int(vx * PLAYER_SPEED)
        for w in walls:
            if player.colliderect(w):
                if vx > 0: player.right = w.left
                if vx < 0: player.left = w.right

        # Y-Kollision
        player.y += int(vy * PLAYER_SPEED)
        for w in walls:
            if player.colliderect(w):
                if vy > 0: player.bottom = w.top
                if vy < 0: player.top = w.bottom

        # 3. Logik (Münzen sammeln)
        remaining_coins = []
        for c in coins:
            if player.colliderect(c):
                score += 1
            else:
                remaining_coins.append(c)
        coins = remaining_coins

        # 4. Zeichnen
        screen.fill((30, 30, 35))
        
        for w in walls:
            pygame.draw.rect(screen, (100, 100, 110), w)
            if debug: pygame.draw.rect(screen, (255, 0, 0), w, 1)

        for c in coins:
            pygame.draw.ellipse(screen, (255, 215, 0), c)

        pygame.draw.rect(screen, (0, 150, 255), player, border_radius=5)

        # HUD
        hud_text = f"Coins: {score}/{total_coins}"
        if not coins:
            hud_text = "GEWONNEN! Drücke ESC."
            pygame.display.set_caption(hud_text)
        
        img = font.render(hud_text, True, (255, 255, 255))
        screen.blit(img, (20, 20))

        pygame.display.flip()

    pygame.quit()