import pygame
import sys
from game import generate_secret_combination, get_player_combination, validate_proposal, combination_length, maximum_number_of_trials, possible_values_in_the_combination

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Créer la fenêtre
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Jeu de Combinaison")

# Police pour le texte
font = pygame.font.SysFont(None, 36)

# Fonction pour afficher le texte
def display_text(text, x, y, color=BLACK):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Fonction pour dessiner un bouton
def draw_button(text, x, y, width, height, color, hover_color):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)
    
    # Changer la couleur du bouton quand la souris est dessus
    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)
    
    # Afficher le texte du bouton
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

    return button_rect

# Fonction principale du jeu
def main_game_loop():
    win = False
    trials = 0
    secret_combination = generate_secret_combination()
    input_text = ""  # Texte saisi par le joueur
    game_over = False
    victory = False

    while True:
        screen.fill(WHITE)  # Remplir la fenêtre avec du blanc

        # Événements de la boucle
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Capture des entrées clavier pour la saisie de la combinaison
            if not game_over and not victory:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]  # Supprimer le dernier caractère
                    elif event.key == pygame.K_RETURN:
                        # Si l'utilisateur appuie sur Enter, vérifier la combinaison
                        if len(input_text) == combination_length:
                            player_combination = [int(c) for c in input_text]
                            correct_position, incorrect_position = validate_proposal(secret_combination, player_combination)

                            if correct_position == 4:
                                victory = True
                            else:
                                trials += 1
                                if trials >= maximum_number_of_trials:
                                    game_over = True

                        input_text = ""  # Réinitialiser après chaque essai
                    elif len(input_text) < combination_length and event.unicode in possible_values_in_the_combination:
                        input_text += event.unicode  # Ajouter un chiffre à l'entrée

        # Affichage des éléments du jeu
        display_text("Entrez une combinaison de 4 chiffres (1-6):", 50, 50)
        display_text(f"Saisie: {input_text}", 50, 100)

        # Affichage du message de victoire
        if victory:
            display_text("Victoire ! Vous avez trouvé la combinaison !", 150, 200, GREEN)

        # Affichage du message Game Over
        elif game_over:
            display_text(f"Game Over ! La combinaison était: {''.join(map(str, secret_combination))}", 150, 200, RED)
        else:
            display_text(f"Essais restants: {maximum_number_of_trials - trials}", 50, 150)

        # Affichage d'un bouton pour recommencer ou quitter
        button_rect = draw_button("Recommencer", 200, 250, 200, 50, GREEN, RED)
        if pygame.mouse.get_pressed()[0] and button_rect.collidepoint(pygame.mouse.get_pos()):
            if game_over or victory:
                main_game_loop()  # Recommencer le jeu

        # Mise à jour de l'affichage
        pygame.display.update()

# Lancer l'application
if __name__ == "__main__":
    main_game_loop()
