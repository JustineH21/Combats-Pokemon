class Error(Exception):
    #Classe permettant de générer des messages d'erreur, ça permettra d'éviter que ça plante
    def __init__(self, msg):
        self.message = msg

class Pokemon:
    def __init__(self, nom:str, pokemon_type:str, niveau:int, EV:list, stats:list, capacites:list, sensibilites:dict):
        self.nom = nom
        self.type = pokemon_type
        self.niveau = 1
        self.xp = 0
        self.xp_max = 100 # xp nécessaires pour monter au prochain niveau
        self.EV = EV
        self.stats = stats
        self.capacites = capacites
        self.sensibilites = sensibilites
        self.PV = self.getPV()
        self.attaque = self.getAttaque()
        self.defense = self.getDefense()
        self.etat = None # pas de problème de statut pour le moment
        self.orientation = None
        self.role = None

    def est_desavantage_type(self, ennemi):
        """ Renvoie True si le Pokémon est sensible au type du Pokémon ennemi, False sinon """
        for type in self.sensibilites:
            if type == ennemi.type and self.sensibilites[type] > 1:
                return True 
        return False

    #fonctions qui permetent de recuperer les valeurs des attributs du pokémon et d'afficher les infos sur le jeu normalement.

    def getNom(self):
        return self.nom
    def getPV(self):
        return self.stats[0]
    def getAttaque(self):
        return self.stats[1]
    def getDefense(self):
        return self.stats[2]
    def getEtat(self):
        return self.etat
    def getNiveau(self):
        return self.niveau
    def getXP(self):
        return self.xp
    def getXPMax(self):
        return self.xp_max
    
    # fonctions qui permettent de modifier les valeurs des attributs du pokémon. 

    def setEtat(self, nouvel_etat):
    #Modifie la valeur de l'attribut etat (ex: poison, paralysie, etc.)
        self.etat = nouvel_etat
    def setPV(self, nb):
        self.PV += nb
        if self.PV < 0:
            self.PV = 0
        elif self.PV > self.stats[0]: # si on a augmenté de plus que ses PV initiaux
            self.PV = self.stats[0]
    def setAttaque(self, nb):
        self.attaque += nb
        if self.attaque < 0:
            self.attaque = 0
        elif self.PV > self.stats[1]: # si on a augmenté de plus que son attaque initiale
            self.PV = self.stats[1]
    def setDefense(self, nb):
        self.defense += nb
        if self.defense < 0:
            self.defense = 0
        elif self.PV > self.stats[2]: # si on a augmenté de plus que sa défense initiale
            self.PV = self.stats[2]
    
class Combat:
    def __init__(self, premier_pokemon_a_jouer_joueur:Pokemon, premier_pokemon_a_jouer_ordi:Pokemon, equipe_joueur:list, equipe_ordi:list):
        self.pokemons_en_jeu = {"joueur": premier_pokemon_a_jouer_joueur, "ordi":premier_pokemon_a_jouer_ordi}
        self.equipes = {"joueur": equipe_joueur, "ordi": equipe_ordi}
        self.player = "joueur" # pour l'instant, le premier à jouer est le joueur

        self.listes_objet = {"joueur": [], "ordi": []}
        # dictionnaire de la forme : {"joueur":[["nom1", Objet, quantite1], ["nom2", Objet, quantite2]], "ordi:[]"}
        for _ in range(5):
            self.ajouter_objet("Potion", "Soins", "joueur")
            self.ajouter_objet("Potion", "Soins", "ordi")
        for _ in range(2):
            self.ajouter_objet("Super Potion", "Soins", "joueur")
            self.ajouter_objet("Super Potion", "Soins", "ordi")

    def ajouter_objet(self, nom, objet_type, equipe):
        """ Crée l'objet puis l'ajoute à la liste des objets de l'équipe """
        trouve = False
        for i in range(len(self.listes_objet[equipe])):
            if self.listes_objet[equipe][i][0] == nom: # si l'objet est déja dans la liste, on ajoute 1 à sa quantité
                self.listes_objet[equipe][i][2] += 1
                trouve = True
        if trouve == False:
            objet = Objets(nom, objet_type, equipe)
            self.listes_objet[equipe].append([objet.nom, objet, 1])
    
    def choisir_nombre(self, texte:str, nb_min:int, nb_max:int):
        """ Demande au joueur de choisir un nombre jusqu'à ce que celui-ci soit valide et renvoie son choix"""
        choix = input(texte)
        correct = False
        while not correct:
            try:
                choix = int(choix)
                if choix <= nb_max and choix >= nb_min:
                    correct = True
                else:
                    print("Ce n'est pas valide. Merci de recommencer")
                    choix = input(texte)
            except:
                print("Ce n'est pas valide. Merci de recommencer")
                choix = input(texte)
            return choix
    
    def choisir_capacite(self, pokemon):
        """ Si c'est le joueur, lui demande de choisir une des capacités du Pokémon en jeu et renvoie le nom de la capacité choisie, sinon, l'ordi choisit la meilleure option """
        for i in range(4): # car chaque Pokémon a 4 capacités
            print(i+1, ":", pokemon.capacites[i])
        choix = self.choisir_nombre("Numéro de l'attaque à effectuer : ", 1, 4)
        return pokemon.capacites[choix - 1]
    
    def choisir_objet(self):
        """ 
        Affiche la liste des objets disponibles si c'est le joueur qui joue et lui demande de choisir.
        Renvoie l'objet choisi (pas son nom) 
        """
        if self.player == "joueur":
            for i in range(len(self.listes_objet[self.player])):
                print(i+1, ":", self.listes_objet[self.player][i][0]) # affiche le nom de l'objet
            choix = self.choisir_nombre("Numéro de l'objet à utiliser : ", 1, len(self.listes_objet[self.player]))
        else:
            pass
        return self.listes_objet[self.player][choix - 1][1] # renvoie l'objet choisi (pas son nom)
    
    def attaquer(self, nom_attaque):
        print("{} ATTAQUE {} !!".format(self.pokemons_en_jeu[self.player].getNom(), nom_attaque))

        if self.player == "joueur":
            cible = self.pokemons_en_jeu["ordi"]
            attaquant = self.pokemons_en_jeu["joueur"]
        else:
            cible = self.pokemons_en_jeu["joueur"]
            attaquant = self.pokemons_en_jeu["ordi"]

        if len(attaque) == 3:  # Si attaque à effets
            effet_attaque = attaque["effet_attaque"]
            valeur_effet = attaque["valeur_attaque"]

            if effet_attaque == 'attaque-e':
                cible.baisserAttaque(valeur_effet)  #baisse attaque de la cible
                print("L'attaque de {} diminue.".format(cible.getNom()))

            elif effet_attaque == 'defense-e':
                cible.baisserDefense(valeur_effet)  #baisse défense de la cible
                print("La défense de {} diminue.".format(cible.getNom()))

            elif effet_attaque == 'attaque+':
                attaquant.augmenterAttaque(valeur_effet)  #augmente attaque de l'attaquant
                print("L'attaque de {} augmente.".format(attaquant.getNom()))

            elif effet_attaque == 'defense+':
                attaquant.augmenterDefense(valeur_effet)  #augmente défense de l'attaquant
                print("La défense de {} augmente.".format(attaquant.getNom()))

            elif effet_attaque == 'poison':
                cible.setEtat({"nom_etat": 'poison', "duree_etat": valeur_effet})
                print("L'énergie de {} est drainée pendant {} tours !".format(cible.getNom(), valeur_effet))

            elif effet_attaque == 'drainage':
                cible.setEtat({"nom_etat": 'drainage', "duree_etat": valeur_effet})
                print("{} est empoisonné pendant {} tours !".format(cible.getNom(), valeur_effet))

            elif effet_attaque == 'paralysie':
                cible.setEtat({"nom_etat": 'paralysie', "duree_etat": valeur_effet})
                print("{} est paralysé pendant {} tours ! Il ne peut plus attaquer".format(cible.getNom(), valeur_effet))

            else:
                raise Error("ERREUR : Type d'attaque {} inconnu !".format(effet_attaque))

        else:  # Si attaque classique
            puissance_attaque = attaque["degats_attaque"]
            degats_infliges = (((( niveau * 0.4 + 2)* attaque*puissance)/ defense)/50)+2 #à moi-meme(chloé), revoir le calcul pour les dégats et appel des attribut/methodes
            degats_infliges = round(degats_infliges)
            cible.baisserHP(degats_infliges)
            print("{} perd {} HP !".format(cible.getNom(), degats_infliges))

    def utiliser_objet(self):
        objet = self.choisir_objet()
        objet.utiliser_objet()

    def changer_pokemon(self, nouveau_pokemon, equipe):
        """ Permet de changer de Pokémon en ayant déjà le nouveau Pokémon à mettre en jeu """
        self.pokemons_en_jeu[equipe] = nouveau_pokemon
        print(equipe + " envoie " + self.pokemons_en_jeu[equipe].getNom() + " au combat !")

    def choisir_option_joueur(self):
        """ Demande au joueur de choisir une action puis lance l'action """
        if self.player == "joueur": # pour être sûr que la fonction n'est appelée que pour le joueur
            print("Que voulez vous faire avec ", self.pokemons_en_jeu[self.player].nom, " ?")
            print("1 : Attaquer")
            print("2 : Utiliser un objet")
            
            # Vérifier s'il y a au moins un Pokémon vivant avant de proposer au joueur de changer de Pokémon
            pokemons_vivants = []
            for p in self.equipes[self.player]:
                 if p.PV > 0 and p != self.pokemons_en_jeu[self.player]:
                     pokemons_vivants.append(p)
            if len(pokemons_vivants) > 0:
                print("3 : Changer de Pokémon")
                choix = self.choisir_nombre("Numéro de l'action à faire : ", 1, 3)
            else:
                choix = self.choisir_nombre("Numéro de l'action à faire : ", 1, 2)
            
            if choix == 1:
                capacite = self.choisir_capacite(self.pokemons_en_jeu[self.player])
                self.attaquer(capacite)
            
            elif choix == 2:
                self.utiliser_objet()

            elif choix == 3:
                # Afficher les choix possibles
                i = 0
                while i < len(pokemons_vivants):
                    pokemon = pokemons_vivants[i]
                    print(str(i + 1) + ". " + pokemon.getNom() + " (PV: " + str(pokemon.getHP()) + ")")
                    i += 1
                pokemon = pokemons_vivants[self.choisir_nombre("Numéro du Pokémon à mettre à la place : ", 1, len(pokemons_vivants) + 1)]
                self.changer_pokemon(pokemon, "joueur")

    def choisir_option_ordi(self): # définir les objets à utiliser !!!
        if self.player == "ordi": # pour être sûre que la fonction n'est appelée que pour l'ordi
            pokemon = self.pokemons_en_jeu["ordi"]
            if pokemon.PV < pokemon.stats[0]/2: # si le Pokémon a moins de la moitié de ses PV
                if pokemon.etat == "Confusion": # s'il est faible et a une altération de statut, on soigne l'altération
                    if pokemon.PV < pokemon.stats[0]/4:
                        self.utiliser_objet()
                    else:
                        self.utiliser_objet()
                elif pokemon == "utile": # si le Pokémon est encore utile, à définir
                    self.utiliser_objet()
                else:
                    self.changer_pokemon()
            elif pokemon.est_desavantage_type(self.pokemons_en_jeu["joueur"]):
                self.changer_pokemon()
            elif pokemon.etat != None: # si le Pokémon a un problème de statut
                if pokemon.etat == "Brûlure" and pokemon.orientation == "Physique":
                    self.utiliser_objet()
                elif pokemon.etat == "Paralysie" and pokemon.role == "Sweeper":
                    self.utiliser_objet()
                elif (pokemon.etat == "Empoisonnement" and pokemon.role == "Tank") or pokemon.etat == "Empoisonnement grave":
                    self.utiliser_objet()
                elif pokemon.etat == "Sommeil":
                    self.utiliser_objet()
                elif pokemon.etat == "Gel":
                    self.utiliser_objet()
            elif self.pokemons_en_jeu["joueur"].PV < self.pokemons_en_jeu["joueur"].stats[0]/7: # si l'ennemi n'a plus que environ 15% de ses PV
                pass # ATTAQUER AVEC UNE ATTAQUE PRIORITAIRE
            elif self.pokemons_en_jeu["joueur"].role == "tank":
                pass # ATTAQUER AVEC UNE ALTÉRATION DE STATUT
            else:
                pass # attaquer ou booster les stats



    def augmenterStatsNiveau(self):
        """ Augmente les stats du Pokémon à chaque montée de niveau. """
        self.attaque += 2 #à moi meme, trouver les maths pour augmenter les stats
        self.defense += 2
        self.vies += 5  # Il récupère aussi des PV quand le pokemon gagne des niveaux 
        print(f"{self.nom} bravo, votre pokemon s'améliore ! ATQ: {self.attaque}, DEF: {self.defense}, PV: {self.HP}")

    def gagnerExp(self, nb):
        """ Ajoute des points d'expérience au Pokémon et gère les montées de niveau. """
        self.xp += nb
        print(f"{self.nom} gagne {nb} XP !")

        # Tant que le pokémon a assez d'XP pour monter de niveau
        while self.xp >= self.xp_max:
            self.xp -= self.xp_max
            self.niveau += 1
            print(f"{self.nom} monte au niveau {self.niveau} !")
            self.xp_max = int(self.xp_max * 1.2)  # XP à atteindre augmente à chaque niveau
            self.augmenterStatsNiveau()

    def gagner_Exp_Selon_Lvl(self, cible):
        xp_gagnee = 20 + (cible.getNiveau() * 5)
        self.gagnerExperience(xp_gagnee)

    def verifier_victoire(self):
        """ Fonction qui vérifie qu'aucun des joueurs n'a gagné, renvoie "égalité" si les deux joueurs ont perdu, "joueur" s'il a gagné, "ordi" s'il a gagné, ou None si le combat n'est pas fini """
        nb_pokemons_en_vie_joueur = 0
        nb_pokemons_en_vie_ordi = 0
        for pokemon in self.equipes["joueur"]:
            if pokemon.PV > 0:
                nb_pokemons_en_vie_joueur += 1
        for pokemon in self.equipes["ordi"]:
            if pokemon.PV > 0:
                nb_pokemons_en_vie_ordi += 1
        
        if nb_pokemons_en_vie_joueur == 0 and nb_pokemons_en_vie_ordi == 0: # s'il y a égalité
            return "égalité"
        elif nb_pokemons_en_vie_joueur == 0:
            return "joueur"
        elif nb_pokemons_en_vie_ordi == 0:
            return "ordi"
        else:
            return None

    def faire_un_combat(self):
        while self.verifier_victoire == None:
            if self.player == "joueur":
                self.choisir_option_joueur()
                self.player = "ordi" # passe au tour de l'ordi
            else:
                self.choisir_option_ordi()
                self.player = "joueur" # passe au tour du joueur
        if self.verifier_victoire == "égalité":
            print("Il y a eu égalité")
        elif self.verifier_victoire == "joueur":
            print("Le joueur a gagné")
        else:
            print("L'ordinateur a gagné")
        
class Objets:
    def __init__(self, nom, objet_type, equipe):
        self.nom = nom
        self.objet_type = objet_type

    def utiliser_objet(self, equipe):
        """
        Retire l'objet utilisé de la liste des objets et effectue l'action liée à cet objet
        """
        for i in range(len(combat.listes_objet[combat.player])):
            # recherche l'objet puis le supprime
            if combat.listes_objet[combat.player][i][0] == self.nom:
                del combat.listes_objet[combat.player][i]
                break

        if self.objet_type == "Soins":
            pokemon_choisi = combat.choisir_pokemon()
            if self.nom == "Potion":
                PV_a_rajouter = 20
            elif self.nom == "Super-potion":
                PV_a_rajouter = 50
            elif self.nom == "Hyper-potion":
                PV_a_rajouter = 200
            elif self.nom == "Potion Max":
                PV_a_rajouter = combat.pokemon_choisi.stats[0]
            
            PV_max_a_rajouter = combat.pokemon_choisi.stats[0] - combat.pokemons_choisi.PV # calcule le nombre max de PV qu'on peut rajouter au Pokémon
            if PV_a_rajouter >= PV_max_a_rajouter:
                combat.pokemon_choisi.PV = combat.pokemon_choisi.stats[0]
            else:
                combat.pokemon_choisi.PV += PV_a_rajouter

        elif self.objet_type == "Réanimation":
            if self.nom == "Rappel" or self.nom == "Rappel Max":
                objet_utilise = False
                while not objet_utilise:
                    pokemon_choisi = combat.choisir_pokemon()
                    if pokemon_choisi.PV == 0:
                        if self.nom == "Rappel":
                            pokemon_choisi.PV = 0.5 * pokemon_choisi.stats[0]
                        else:
                            pokemon_choisi.PV = pokemon_choisi.stats[0]
                        objet_utilise = True
                    else:
                        print("Ce Pokémon n'est pas KO, merci d'en choisir un autre qu'il l'est")
            
            elif self.nom == "Cendre sacrée":
                for pokemon in combat.equipes[combat.player]:
                    if pokemon.PV == 0:
                        pokemon.PV = pokemon.stats[0]

        elif self.objet_type == "PPS":
            if self.nom == "Huile":
                PP_a_ajouter = ["une", 10]
            elif self.nom == "Huile Max":
                PP_a_ajouter = ["une", "max"]
            elif self.nom == "Élixir":
                PP_a_ajouter = ["toutes", 10]
            elif self.nom == "Élixir Max":
                PP_a_ajouter = ["toutes", "max"]    

            pokemon = combat.choisir_pokemon()
            capacite = combat.choisir_capacite(pokemon)
            pokemon.capacites[capacite]["PP"] += PP_a_ajouter[1]


# pour les EV et les stats : [HP, Attaque, Défense, Attaque Spé, Défense Spé, Vitesse]
avaltout1 = Pokemon("Avaltout1", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout2 = Pokemon("Avaltout2", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout3 = Pokemon("Avaltout3", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout4 = Pokemon("Avaltout4", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout5 = Pokemon("Avaltout5", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout6 = Pokemon("Avaltout6", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], ["Détricano", "Rest", "Sludge Bomb", "Séisme"], {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})

combat = Combat(avaltout1, avaltout4, [avaltout1, avaltout2, avaltout3], [avaltout4, avaltout5, avaltout6])
#objet = Objets("objet", "joueur")