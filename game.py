import numpy as np
import random
combination_length = 4
maximum_number_of_trials = 10
possible_values_in_the_combination = [value for value in range(1,7)]

def generate_secret_combination():
    return [random.choice(possible_values_in_the_combination) for _ in range(combination_length)]

def get_player_combination():
    while True:
        combinaison = input("Veuillez entrer une combinaison de 4 chiffres : ")
        
        # Vérifie si la combinaison est valide (4 chiffres uniquement)
        if len(combinaison) == 4 and combinaison.isdigit() and all(int(c) in possible_values_in_the_combination for c in combinaison):
            return [int(c) for c in combinaison]
        elif len(combinaison) < 4:
            print("combinaison trop court")
        elif len(combinaison) > 4 :
            print("combinaison trop long")
        else:
            print("Combinaison invalide. Assurez-vous de saisir exactement 4 chiffres dans la plage de 1 à 6")
def validate_proposal(secret_combination,combination_proposal):
    correct_position = 0
    incorrect_position = 0

    new_secret_combination = secret_combination[:]
    new_combination_proposal = combination_proposal[:]


    for index, val in enumerate(combination_proposal):
        if secret_combination[index] == val:
            correct_position +=1
            new_combination_proposal[index] = None
            new_secret_combination[index] = None

    for index in range(combination_length):
        if new_combination_proposal[index] is not None:
            if new_combination_proposal[index] in new_secret_combination:
                incorrect_position +=1
                new_secret_combination[new_secret_combination.index(new_combination_proposal[index])] = None

    return correct_position, incorrect_position

def main_game_loop():
    win = False
    trials = 0
    secret_combination = generate_secret_combination()


    while( win != True and trials < maximum_number_of_trials):

        player_combination = get_player_combination()
        correct_position, incorrrect_position =validate_proposal(secret_combination,player_combination)

        if (correct_position == 4) :
            print("Victoire !")
            win = True
        else :
            trials +=1
            print("Nombre de chiffres bien placés : {}".format(correct_position))
            print("Nombre de chiffres present mais mal placés {}".format(incorrrect_position))
            print("Il vous reste {} essais".format(maximum_number_of_trials-trials))
    if( trials == maximum_number_of_trials):
        print("Game over !!!")
        print("Le resultat est : {}".format(secret_combination))
    



