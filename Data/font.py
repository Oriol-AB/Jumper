import pygame
import sys

pygame.init()

pygame.font.init()

display = pygame.display.set_mode((900, 600))

font = pygame.font.Font("Font/PressStart2P-Regular.ttf", 60)

txt = font.render("Mantén pulsado para cargar la barra", False, (0, 0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
            pygame.quit()

    
    pygame.image.save(txt, "tut.png")

    sys.exit()

    
