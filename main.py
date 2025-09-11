class Pokemon:
    def __init__(self, nom:str, pokemon_type:str, niveau:int, EV:list, stats:list, capacites:list, sensibilites:dict):
        self.nom = nom
        self.type = pokemon_type
        self.niveau = niveau
        self.EV = EV
        self.stats = stats
        self.capacites = capacites
        self.sensibilites = sensibilites
        self.PV = self.stats[0]

class Combat:
    def __init__(self, premier_pokemon_a_jouer_joueur:Pokemon, premier_pokemon_a_jouer_ordi:Pokemon, equipe_joueur:list, equipe_ordi:list):
        self.pokemons_en_jeu = {"joueur": premier_pokemon_a_jouer_joueur, "ordi":premier_pokemon_a_jouer_ordi}
        self.equipes = {"joueur": equipe_joueur, "ordi": equipe_ordi}
        self.player = "joueur" # pour l'instant, le premier à jouer est le joueur
        self.listes_objet = {"joueur": {}, "ordi": {}}

    def choisir_option(self):
        """
        Demande au joueur de choisir une action puis lance l'action
        """
        if self.player == "joueur":
            print("Que voulez vous faire avec ", self.pokemons_en_jeu[self.player].nom, " ?")
            print("1 : Attaquer")
            print("2 : Utiliser un objet")
            print("3 : Changer de Pokémon")
            choix = input("Numéro de l'action à faire : ")
            
            if choix == "1":
                for i in range(4):
                    print(i+1, ":", self.pokemons_en_jeu[self.player].capacites[i])
                choix = input("Numéro de l'attaque à effectuer : ")
                self.attaquer(self.pokemons_en_jeu[self.player].capacites[int(choix) - 1])
            
            elif choix == "2":
                self.utiliser_objet()

            elif choix == "3":
                numero_a_entrer = 1
                pokemon_affiches = []
                for pokemon in self.equipes[self.player]:
                    if not pokemon == self.pokemons_en_jeu[self.player]:
                        print(numero_a_entrer, ":", pokemon.nom) # affiche les autres Pokémon de l'équipe (pas celui en jeu)
                        numero_a_entrer += 1
                        pokemon_affiches.append(pokemon.nom)
                choix_pokemon = input("Numéro du Pokémon à mettre en jeu : ")
                pokemon = pokemon_affiches[int(choix_pokemon) - 1]
                self.changer_pokemon(pokemon, "joueur")

    def attaquer(self, choix):
        pass

    def utiliser_objet(self):
        pass

    def changer_pokemon(self, nouveau_pokemon, equipe):
        pass

class Objets:
    def __init__(self, nom, objet_type, equipe):
        self.nom = nom
        self.objet_type = objet_type
        if self.nom in combat.listes_objet[equipe]:
            combat.listes_objet[equipe][nom] += 1
        else:
            combat.listes_objet[equipe][nom] = 1

    def utiliser_objet(self, equipe):
        """
        Retire un à la liste des objets et effectue l'action liée à cet objet
        """
        combat.listes_objet[equipe][self.nom] -= 1

        if self.objet_type == "Soins":
            if self.nom == "Potion":
                PV_a_rajouter = 20
            elif self.nom == "Super-potion":
                PV_a_rajouter = 50
            elif self.nom == "Hyper-potion":
                PV_a_rajouter = 200
            elif self.nom == "Potion Max":
                PV_a_rajouter = "max"
            
            PV_max_a_rajouter = combat.pokemons_en_jeu[equipe].stats[0] - combat.pokemons_en_jeu[equipe].PV # calcule le nombre max de PV qu'on peut rajouter au Pokémon
            if PV_a_rajouter >= PV_max_a_rajouter:
                combat.pokemons_en_jeu[equipe].PV = combat.pokemons_en_jeu[equipe].stats[0]
            else:
                combat.pokemons_en_jeu[equipe].PV += PV_a_rajouter

# pour les EV et les stats : [HP, Attaque, Défense, Attaque Spé, Défense Spé, Vitesse]
avaltout1 = Pokemon("Avaltout1", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout2 = Pokemon("Avaltout2", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout3 = Pokemon("Avaltout3", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout4 = Pokemon("Avaltout4", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout5 = Pokemon("Avaltout5", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout6 = Pokemon("Avaltout6", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})

combat = Combat(avaltout1, avaltout4, [avaltout1, avaltout2, avaltout3], [avaltout4, avaltout5, avaltout6])
objet = Objets("objet", "joueur")