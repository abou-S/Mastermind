import pygame
import random

class Game:
    def __init__(self):
        self.secret_combination = self.generate_secret_combination()
        print(self.secret_combination)
        self.trials = 10
        self.correct_position = 0
        self.incorrect_position = 0
        self.player_combination = None
        self.button_rect = pygame.Rect(390, 255, 160, 40)
        self.button_text = "Recommencer"
        self.font = pygame.font.Font(None, 32)
        self.smaller_font = pygame.font.Font(None, 20)
        self.display_text = ""
    
    def get_trials(self):
        """Récupérer le nombre d'essais restants."""
        return self.trials 
    
    def get_correct_position(self):
        """Récupérer le nombre de chiffres bien placés."""
        return self.correct_position

    def generate_secret_combination(self):
        """Génère la combinaison secrète de 4 chiffres."""
        return [random.choice(range(1, 7)) for _ in range(4)]

    def handle_restart_button(self, pos):
        """Vérifie si le bouton de redémarrage a été cliqué."""
        return self.button_rect.collidepoint(pos)

    def reset_game(self):
        """Réinitialise le jeu avec une nouvelle combinaison secrète."""
        self.secret_combination = self.generate_secret_combination()
        print(self.secret_combination)
        self.trials = 10
        self.correct_position = 0
        self.incorrect_position = 0
        self.player_combination = None

    def process_input(self, input_text):
        """Traite l'entrée du joueur et met à jour le jeu."""
        self.player_combination = self.get_player_combination(input_text)
        if self.player_combination:
            self.correct_position, self.incorrect_position = self.validate_proposal(self.secret_combination, self.player_combination)
            self.trials -= 1
            self.display_text = input_text


    def get_player_combination(self, combinaison):
        """Vérifie si la combinaison est valide (4 chiffres entre 1 et 6)."""
        if len(combinaison) == 4 and combinaison.isdigit() and all(int(c) in range(1, 7) for c in combinaison):
            return [int(c) for c in combinaison]
        return 0

    def validate_proposal(self, secret_combination, combination_proposal):
        """Valide la proposition du joueur par rapport à la combinaison secrète."""
        correct_position = 0
        incorrect_position = 0
        new_secret_combination = secret_combination[:]
        new_combination_proposal = combination_proposal[:]

        # Vérifie les bonnes positions
        for index, val in enumerate(combination_proposal):
            if secret_combination[index] == val:
                correct_position += 1
                new_combination_proposal[index] = None
                new_secret_combination[index] = None

        # Vérifie les mauvaises positions
        for index in range(4):
            if new_combination_proposal[index] is not None:
                if new_combination_proposal[index] in new_secret_combination:
                    incorrect_position += 1
                    new_secret_combination[new_secret_combination.index(new_combination_proposal[index])] = None

        return correct_position, incorrect_position

    def draw_input_box(self, screen, input_box, color, text):
        """Dessine la boîte de saisie pour la combinaison du joueur."""
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = self.font.render(text, True, pygame.Color("black"))
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

    def draw_info(self, screen, screen_width, screen_height):
        """Affiche les informations du jeu à l'écran : essais restants, résultats, messages d'erreur."""
        # Afficher le nombre d'essais restants
        tiltle_text = self.font.render(f"Entrez votre combinaison de 4 chiffres (de 1 à 6)", True, pygame.Color("black"))
        screen.blit(tiltle_text, (10, 30))

        # Afficher le nombre d'essais restants
        trials_text = self.font.render(f"Essais restants: {self.trials}", True, pygame.Color("black"))
        screen.blit(trials_text, (10, screen_height -30))

        if self.player_combination:
            # Afficher les résultats du dernier essai
            if self.correct_position == 4:
                # Le joueur a gagné
                victory_text = self.font.render("Bravo ! Vous avez gagné !", True, pygame.Color("green"))
                screen.blit(victory_text, ((screen_width - victory_text.get_width()) // 2, 150))
            elif self.trials == 0:
                # Le joueur a perdu
                game_over_text = self.font.render("Game over !", True, pygame.Color("red"))
                screen.blit(game_over_text, ((screen_width - game_over_text.get_width()) // 2, 150))
                result_text = self.font.render(f"La combinaison secrète était: {''.join(map(str,self.secret_combination))}", True, pygame.Color("green"))
                screen.blit(result_text, ((screen_width - result_text.get_width()) // 2, 190))


            else :
                # Afficher les résultats du dernier essai (incorrects et bien placés)
                if self.player_combination:
                    incorrect_proposal_text = self.smaller_font.render(
                        f"la proposition {self.display_text} est incorrecte", True, pygame.Color("red"))
                    screen.blit(incorrect_proposal_text, ((screen_width - incorrect_proposal_text.get_width()) // 2, 150))

                    correct_position_text = self.smaller_font.render(
                        f"Chiffres bien placés: {self.correct_position}", True, pygame.Color("black"))
                    screen.blit(correct_position_text, ((screen_width - correct_position_text.get_width()) // 2, 180))

                    incorrect_position_text = self.smaller_font.render(
                        f"Chiffres présents mais mal placés: {self.incorrect_position}", True, pygame.Color("black"))
                    screen.blit(incorrect_position_text, ((screen_width - incorrect_position_text.get_width()) // 2, 210))
        elif self.player_combination == 0:
            # Saisi invalide
            saisie_invalide = self.smaller_font.render("Saisie invalide, veuillez choisir des chiffres compris entre 1 et 6.", True, pygame.Color("orange"))
            screen.blit(saisie_invalide, ((screen_width - saisie_invalide.get_width()) // 2, 150))

    def update_button(self, screen):
        """Mise à jour de l'affichage du bouton 'Recommencer'."""
        pygame.draw.rect(screen, pygame.Color("blue"), self.button_rect)
        button_surface = self.font.render(self.button_text, True, pygame.Color("white"))
        button_text_rect = button_surface.get_rect(center=self.button_rect.center)
        screen.blit(button_surface, button_text_rect)
