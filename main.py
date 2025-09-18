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
    def __init__(self, premier_pokemon_a_jouer_joueur:Pokemon, premier_pokemon_a_jouer_ordi:Pokemon, equipe_joueur:list, equipe_ordi:list,nouveau_pokemon: str, equipe: list):
        self.pokemons_en_jeu = {"joueur": premier_pokemon_a_jouer_joueur, "ordi":premier_pokemon_a_jouer_ordi}
        self.equipes = {"joueur": equipe_joueur, "ordi": equipe_ordi}
        self.player = "joueur" # pour l'instant, le premier à jouer est le joueur
        self.listes_objet = {"joueur": {}, "ordi": {}}

        self.niveau = 1
        self.xp = 0
        self.xp_max = 100 #xp nécessaires pour prochain niveau

        self.nouveau_pokemon = nouveau_pokemon
        self.equipe = equipe
        self.pokemon_actif = self._equipe[0]  # Le premier Pokémon est actif par défaut


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


    def getPokemonActif(self):
        return self.pokemon_actif

    def getEquipe(self):
        return self.equipe

    def changerPokemon(self):
    """ Permet au joueur de changer de Pokémon parmi Pokémon encore vivants. """
    print("self.nouveau_pokemon + ", qui veux-tu envoyer au combat ?")

    # Construction de la liste des Pokémon vivants (sauf le Pokémon déjà actif)
    pokemons_vivants = []
    for p in self.equipe:
        if p.KO() == False and p != self.pokemon_actif:
            pokemons_vivants.append(p)

    # Vérifier s'il y a au moins un Pokémon vivant
    if len(pokemons_vivants) == 0:
        print("Aucun autre Pokémon vivant dans l’équipe !")
        return False

    # Afficher les choix possibles
    i = 0
    while i < len(pokemons_vivants):
        pokemon = pokemons_vivants[i]
        print(str(i + 1) + ". " + pokemon.getNom() + " (PV: " + str(pokemon.getHP()) + ")")
        i = i + 1

    # Demande au joueur de choisir
    choix = 0
    while choix < 1 or choix > len(pokemons_vivants):
        saisi = input("Entrez le numéro du Pokémon à envoyer : ")
        choix = int(saisi)

    # Effectue changement Pokémon actif
    self.pokemon_actif = pokemons_vivants[choix - 1]
    print(self.nom + " envoie " + self.pokemon_actif.getNom() + " au combat !")
    return True

    self.pokemon_actif = pokemons_vivants[choix - 1]
    print(f"{self.nom} envoie {self.pokemon_actif.getNom()} au combat !")
    return True

    
    
    
    #Ce que Chloé a ajouté (pour qu'on se retrouve dans tout ça)____________________________________________________________________________________________________________________________________________________________
    
    
    #fonctions qui permet de recuperer les valeurs des attributs du pokémon et d'afficher les infos sur le jeu normalement.

    def getNom(self):
        return self.nom

    def getHP(self):
        return self.hp

    def getAttaque(self):
        return self.attaque

    def getDefense(self):
        return self.defense

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


    def baisserHP(self, nb):
        self.HP -= nb
        if self.HP < 0:
            self.HP = 0


    def baisserAttaque(self, nb):
        self.attaque -= nb
        if self.attaque < 0:
            self.attaque = 0


    def baisserDefense(self, nb):
        self.defense -= nb
        if self.defense < 0:
            self.defense = 0
            
    def baisserDefenseSpe(self, nb):
        self.defenseSpe -= nb
        if self.defenseSpe < 0:
            self.defenseSpe = 0 
    def baisserAttaqueSpe(self, nb):
        self.attaqueSpe -= nb

    def augmenterHP(self, nb):
        self.HP += nb
    # à moi-meme (chloe) limiter ici avec un max (self._vies = min(self._vies, self._vies_max(?)) 
    def augmenterAttaque(self, nb):
        self.attaque += nb

    def augmenterDefense(self, nb):
        self.defense += nb

    def augmenterAttSpe(self, nb):
        self.attaqueSpe += nb
        
    def augmenterDefSpe(self, nb):
        self.defenseSpe += nb 

    
    def attaquer(self, choix):
        nom_attaque = attaque["nom_attaque"]
        print("{} ATTAQUE {} !!".format(attaquant.getNom(), nom_attaque))

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




    
#________________________________________________________________________________________________________________________________________________________________________________________________________________ 
    
    
    
    
    
    
    def utiliser_objet(self):
        pass

    def changer_pokemon(self, nouveau_pokemon, equipe):
        pass
        

#_________________________________________________________________________________________________________________________________________________________________________________________________________________

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
