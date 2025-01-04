import pygame
import sys
from game import Game

# Initialisation de Pygame
pygame.init()

# Configuration de la fenêtre
screen_width = 560
screen_height = 300
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Mastermind')

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)


# Paramètres du champ de saisie
input_box_width = 100
input_box_height = 40
x = (screen_width - input_box_width) // 2
y = 100
input_box = pygame.Rect(x, y, input_box_width, input_box_height)

color_inactive = GRAY
color_active = GREEN
color = color_inactive
text = ''
active = False

# Initialiser le jeu
game = Game()

# Boucle principale du jeu
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = True
                color = color_active
            else:
                active = False
                color = color_inactive
            if game.handle_restart_button(event.pos):
                game.reset_game()
                text = ''


        if event.type == pygame.KEYDOWN:
            if active and (game.get_trials() > 0 | game.get_correct_position() != 4):
                if event.key == pygame.K_RETURN:
                    game.process_input(text)
                    text = ''
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                elif len(text) < 4:
                    text += event.unicode

    # Mise à jour de l'écran
    screen.fill(WHITE)
    game.draw_input_box(screen, input_box, color, text)
    game.draw_info(screen, screen_width, screen_height, )
    game.update_button(screen)

    pygame.display.flip()
    clock.tick(30)
