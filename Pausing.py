import pygame 
from os import sys

clock = pygame.time.Clock()

def pause(screen, score):
    paused = True
    font = pygame.font.SysFont("Verdana", 17)
    text = font.render(f"Your score: {score}, press C to continue", True, "black")
    text_rect = text.get_rect(center=(200, 150))

    while paused:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                                paused = False
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
        screen.fill("white")
        screen.blit(text, text_rect)
        pygame.display.update()
        clock.tick(5)
                        