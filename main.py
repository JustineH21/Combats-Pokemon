from random import *

class Error(Exception):
    #Classe permettant de générer des messages d'erreur, ça permettra d'éviter que ça plante
    def __init__(self, msg):
        self.message = msg

class Pokemon:
    def __init__(self, nom:str, pokemon_type:str, EV:list, stats:list, capacites:list, sensibilites:dict):
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
        self.etat = None # pas de problème de statut pour le moment, après, dictionnaire : {"nom_etat": "...", "duree_etat": ...}
        self.orientation = None
        self.role = None
        self.objet_tenu = None
        self.statut = None  
        self.statut_duree = 0  

    def est_desavantage_type(self, ennemi):
        """ Renvoie True si le Pokémon est sensible au type du Pokémon ennemi, False sinon """
        for type in self.sensibilites:
            if type == ennemi.type and self.sensibilites[type] > 1:
                return True 
        return False
    
    def efficacite_type(self, type_attaque:str):
        """ Renvoie la sensibilité d'un Pokémon à une attaque """
        for type in self.sensibilites:
            if type_attaque == type:
                return self.sensibilites[type]
        return 1

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
    def estKO(self):
        return self.PV <= 0
    def getCapacites(self):
        return self.capacites
    
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

class Capacite:
    def __init__(self, nom, type, classe, PP, probabilite, puissance, priorite, effet_attaque=None, valeur_effet=None,statut=None, statut_chance=0 ):
        self.nom = nom
        self.type = type
        self.classe = classe
        self.PP = PP
        self.probabilite = probabilite
        self.puissance = puissance
        self.priorite = priorite
        self.effet_attaque = effet_attaque
        self.valeur_effet = valeur_effet
        self.statut = statut  # nouveau
        self.statut_chance = statut_chance #nouveau 
    
    #nouveau 
    if combat.peut_agir(self.pokemons_en_jeu["joueur"]):
        action_joueur[1].utiliser_capacite()
    else:
        print(f"{self.pokemons_en_jeu['joueur'].nom} ne peut pas agir ce tour.")

    if self.statut and random.random() < self.statut_chance:
        combat.infliger_statut(pokemon_cible, self.statut)

    
    
    def utiliser_capacite(self, attaquant:Pokemon, cible:Pokemon):
        print("{} ATTAQUE {} !!".format(self.pokemons_en_jeu[self.player].getNom(), self.nom))
        
        if self.effet_attaque != None and self.valeur_effet != None:  # Si attaque à effets
            if self.effet_attaque == 'attaque-e':
                cible.setAttaque(-1 * self.valeur_effet)  #baisse attaque de la cible
                print("L'attaque de {} diminue.".format(cible.getNom()))

            elif self.effet_attaque == 'defense-e':
                cible.setDefense(-1 * self.valeur_effet)  #baisse défense de la cible
                print("La défense de {} diminue.".format(cible.getNom()))

            elif self.effet_attaque == 'attaque+':
                attaquant.setAttaque(self.valeur_effet)  #augmente attaque de l'attaquant
                print("L'attaque de {} augmente.".format(attaquant.getNom()))

            elif self.effet_attaque == 'defense+':
                attaquant.setDefense(self.valeur_effet)  #augmente défense de l'attaquant
                print("La défense de {} augmente.".format(attaquant.getNom()))

            elif self.effet_attaque == 'poison':
                cible.setEtat({"nom_etat": 'poison', "duree_etat": self.valeur_effet})
                print("{} est empoisonné pendant {} tours !".format(cible.getNom(), self.valeur_effet))

            elif self.effet_attaque == 'drainage':
                cible.setEtat({"nom_etat": 'drainage', "duree_etat": self.valeur_effet})
                print("L'énergie de {} est drainée pendant {} tours !".format(cible.getNom(), self.valeur_effet))

            elif self.effet_attaque == 'paralysie':
                cible.setEtat({"nom_etat": 'paralysie', "duree_etat": self.valeur_effet})
                print("{} est paralysé pendant {} tours ! Il ne peut plus attaquer".format(cible.getNom(), self.valeur_effet))

            else:
                raise Error("ERREUR : Type d'attaque {} inconnu !".format(self.effet_attaque))

        else:  # Si attaque classique
            if self.type == "Spéciale":
                attaque = attaquant.stats[3]
                defense = cible.stats[4]
            else:
                attaque = attaquant.stats[1]
                defense = cible.stats[2]
            degats_infliges = abs(abs(abs((abs(attaquant.niveau * 0.4) + 2) * attaque * self.puissance)/defense)/50) + 2
            stab = 1
            if attaquant.type == self.type:
                stab = 1.5
            efficacite = cible.efficacite_type(self.type)
            coup_critique = 1
            if random.randint(1, 16) == 1:
                coup_critique = 1.5
                print("COUP CRITIQUE !")
            nombre = random.randint(85, 100)/100
            cm = stab * efficacite * coup_critique * nombre
            degats_infliges = abs(degats_infliges * cm)
            if cible.objet_tenu != None and self.classe == "Physique": 
                # si la cible porte un casque brut, elle ne peut pas perdre plus de 1/6 de ses PV maximums lors d'une attaque physique
                if cible.objet_tenu.nom == "Casque Brut" and degats_infliges > cible.stats[0]/6:
                    print("{} utilise son Casque Brut pour se protéger".format(cible.getNom()))
                    degats_infliges = cible.stats[0]/6
            cible.setPV(-1 * degats_infliges)
            print("{} perd {} HP !".format(cible.getNom(), degats_infliges))


        def capacites_noms(liste_noms):
            return [CAPACITES[nom] for nom in liste_noms if nom in CAPACITES]

        #nouveau 
        def infliger_statut(self, pokemon, statut):
            if pokemon.statut is None:
                pokemon.statut = statut
                if statut in ["Sommeil"]:
                    pokemon.statut_duree = random.randint(
                        STATUTS[statut]["duree_min"], STATUTS[statut]["duree_max"])
                elif statut == "Gel":
                    pokemon.statut_duree = -1  # on le conserve tant qu'il ne se dégèle pas
                print(f"{pokemon.nom} est maintenant {statut.lower()} !")
            else:
                print(f"{pokemon.nom} est déjà affecté par {pokemon.statut.lower()}.")

            #nouveau
        def peut_agir(self, pokemon):
            statut = pokemon.statut
            if statut is None:
                return True
    
            effets = STATUTS[statut]
        
            if effets["effet"] == "inactif":
                print(f"{pokemon.nom} dort et ne peut pas attaquer !")
                return False
        
            if effets["effet"] == "inactif_prob":
                if random.random() > effets["probabilite"]:
                    print(f"{pokemon.nom} est gelé et ne peut pas attaquer !")
                    return False
                else:
                    print(f"{pokemon.nom} brise la glace et peut attaquer !")
                    pokemon.statut = None
                    return True
        
            if effets["effet"] == "chance_inactif":
                if random.random() < effets["probabilite"]:
                    print(f"{pokemon.nom} est paralysé et ne peut pas attaquer !")
                    return False
        
            return True


    


class Combat:
    def __init__(self, premier_pokemon_a_jouer_joueur:Pokemon, premier_pokemon_a_jouer_ordi:Pokemon, equipe_joueur:list, equipe_ordi:list, action_retardee: dict):
        self.pokemons_en_jeu = {"joueur": premier_pokemon_a_jouer_joueur, "ordi":premier_pokemon_a_jouer_ordi}
        self.equipes = {"joueur": equipe_joueur, "ordi": equipe_ordi}
        self.player = "joueur" # pour l'instant, le premier à jouer est le joueur
        self.action_retardee = {
            "joueur": None,
            "ordi": None }
        self.listes_objet = {"joueur": [], "ordi": []}
        # dictionnaire de la forme : {"joueur":[["nom1", Objet, quantite1], ["nom2", Objet, quantite2]], "ordi:[]"}
        for _ in range(5):
            self.ajouter_objet("Potion", "Soins", "joueur", 20)
            self.ajouter_objet("Potion", "Soins", "ordi", 20)
        for _ in range(2):
            self.ajouter_objet("Super Potion", "Soins", "joueur", 50)
            self.ajouter_objet("Super Potion", "Soins", "ordi", 50)

    def ajouter_objet(self, nom, objet_type, equipe, info):
        """ Crée l'objet puis l'ajoute à la liste des objets de l'équipe """
        trouve = False
        for i in range(len(self.listes_objet[equipe])):
            if self.listes_objet[equipe][i][0] == nom: # si l'objet est déja dans la liste, on ajoute 1 à sa quantité
                self.listes_objet[equipe][i][2] += 1
                trouve = True
        if trouve == False:
            objet = Objets(nom, objet_type, equipe, info)
            self.listes_objet[equipe].append([objet.nom, objet, 1])
        self.listes_objet[equipe][1].quantite += 1
    
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
    
    def choisir_objet(self, type = None):
        """ 
        Affiche la liste des objets disponibles si c'est le joueur qui joue et lui demande de choisir.
        Renvoie l'objet choisi (pas son nom) 
        """
        if self.player == "joueur":
            for i in range(len(self.listes_objet[self.player])):
                print(i+1, ":", self.listes_objet[self.player][i][0]) # affiche le nom de l'objet
            choix = self.choisir_nombre("Numéro de l'objet à utiliser : ", 1, len(self.listes_objet[self.player]))
        else:
            if type == "PV":
                meilleur_objet = None
                liste = []
                PV_necessaire = self.pokemons_en_jeu["ordi"].stats[0] - self.pokemons_en_jeu["ordi"].PV
                PV_max = 0 # le maximum que l'on peut rajouter en PV avec l'objet le plus haut (hors Potion Max)
                for obj in self.listes_objet["ordi"][1]:
                    if obj.objet_type == "Soins":
                        if obj.info == "max":
                            coeff = None
                        elif obj.info > PV_max:
                            PV_max = obj.info
                        efficacite = 1 - abs(obj.info - PV_necessaire)/PV_necessaire
                        coeff = efficacite*0.7 + obj.quantite*0.3
                        liste.append([obj, coeff]) # crée une liste des objets de soins et de leur coeff

                if len(liste) == 0:
                    return False

                meilleur_objet = liste[0]    
                for obj, coeff in liste:
                    if coeff == None:
                        if obj.quantite < 3: # si on n'a que 1 ou 2 Potion Max
                            ratio_max = 0.2 # il faut que le ratio entre la meilleure autre potion et les PV nécessaires soit inférieur à 20%
                            PV_restants_min = 100 # le Pokémon doit avoir besoin d'encore au moins 100 PV après la meilleure autre potion
                        elif obj.quantite >= 7:
                            ratio_max = 0.5
                            PV_restants_min = 50
                        else:
                            ratio_max = 0.33
                            PV_restants_min = 75
                        
                        ratio = PV_max / PV_necessaire
                        PV_restants = PV_necessaire - PV_max
                        if ratio <= ratio_max and PV_restants >= PV_restants_min:
                            meilleur_objet = obj

                    elif coeff > meilleur_objet[1]:
                        meilleur_objet = obj

                objet = meilleur_objet
                
            else:
                total_soin = False
                for obj in self.listes_objet["ordi"][1]:
                    if obj.info == type:
                        objet = obj
                    elif obj.nom == "Total Soin":
                        total_soin = obj
                
                if objet == None and total_soin != False: # si on n'a pas le spray nécessaire mais qu'on a un Total Soin
                    objet = total_soin
                
                elif objet == None: # si on n'a toujours rien qui peut soigner l'altération de statut, on renvoie False
                    return False
                
        return self.listes_objet[self.player][choix - 1][1] # renvoie l'objet choisi (pas son nom)

    def utiliser_objet(self, objet):
        objet.utiliser_objet()

    def choisir_pokemon_a_mettre_en_jeu_ordi(self, liste):
        """ Choisit le meilleur Pokémon à mettre en jeu à partir de la liste """
        if len(liste) > 1:
            liste2 = []
            for pokemon in liste:
                ratio_PV = pokemon.PV / pokemon.stats[0]
                faiblesses = 0
                forces = 0
                nb_ennemis = 0
                for ennemi in self.equipes["joueur"]:
                    if ennemi.PV > 0:
                        if pokemon.est_desavantage_type(ennemi):
                            faiblesses += 1
                        if ennemi.est_desavantage_type(pokemon):
                            forces += 1
                    nb_ennemis += 1
                faiblesses = faiblesses / nb_ennemis
                forces = forces / nb_ennemis
                coeff = ratio_PV - faiblesses + 0.5 * forces
                liste2.append([pokemon, coeff])

            meilleur_pokemon = liste2[0]
            if liste2[1][1] > meilleur_pokemon[1]: # si le coeff du deuxième Pokémon est supérieur au coeff du premier Pokémon (car seulement 3 Pokémon par équipe)
                meilleur_pokemon = liste2[1]

        elif len(liste) == 0:
                return False
        else:
            meilleur_pokemon = liste[0]

        self.changer_pokemon(meilleur_pokemon)
        return True

    def changer_pokemon(self, nouveau_pokemon, equipe):
        """ Permet de changer de Pokémon en ayant déjà le nouveau Pokémon à mettre en jeu """
        self.pokemons_en_jeu[equipe] = nouveau_pokemon
        print(equipe + " envoie " + self.pokemons_en_jeu[equipe].getNom() + " au combat !")

    def liste_pokemons_vivants_pas_en_jeu(self):
        pokemons_vivants = []
        for p in self.equipes[self.player]:
            if p.PV > 0 and p != self.pokemons_en_jeu[self.player]:
                pokemons_vivants.append(p)
        return pokemons_vivants

    def choisir_option_joueur(self):
        """ Demande au joueur de choisir une action puis lance l'action """
        if self.player == "joueur": # pour être sûr que la fonction n'est appelée que pour le joueur
            print("Que voulez vous faire avec ", self.pokemons_en_jeu[self.player].nom, " ?")
            print("1 : Attaquer")
            print("2 : Utiliser un objet")
            
            # Vérifier s'il y a au moins un Pokémon vivant avant de proposer au joueur de changer de Pokémon
            pokemons_vivants = self.liste_pokemons_vivants_pas_en_jeu()
            if len(pokemons_vivants) > 0:
                print("3 : Changer de Pokémon")
                choix1= self.choisir_nombre("Numéro de l'action à faire : ", 1, 3)
            else:
                choix1 = self.choisir_nombre("Numéro de l'action à faire : ", 1, 2)

            if choix1 == 1:
                choix2 = self.choisir_capacite(self.pokemons_en_jeu[self.player])
            
            elif choix1 == 2:
                choix2 = self.choisir_objet()

            elif choix1 == 3:
                i = 0
                while i < len(pokemons_vivants):
                    pokemon = pokemons_vivants[i]
                    print(str(i + 1) + ". " + pokemon.getNom() + " (PV : " + str(pokemon.getHP()) + ")")
                    i += 1
                choix2 = pokemons_vivants[self.choisir_nombre("Numéro du Pokémon à envoyer : ", 1, len(pokemons_vivants) + 1)]

            return [choix1, choix2]

    def choisir_option_ordi(self): # définir les objets à utiliser !!!
        """ Fait choisir une option à l'ordi en fonction de la situation """
        if self.player == "ordi": # pour être sûre que la fonction n'est appelée que pour l'ordi
            pokemon = self.pokemons_en_jeu["ordi"]
            ennemi = self.pokemons_en_jeu["joueur"] # pour que ça soit plus lisible
            action_faite = False
            # on met toutes les options possibles en True, c'est-à-dire qu'on les considère comme faisable
            # mais si jamais une action n'est pas faisable (par exemple on n'a pas de potion donc on ne peut pas se soigner), l'option passe en False
            # c'est pour éviter que l'option soit reprise à chaque fois, même si elle n'est pas possible => éviter boucle infinie
            option1 = [True, True] # car il y a deux sous-possibilités
            option2 = True
            option3 = [True, True, True, True, True]
            option4 = True
            option5 = True
            while action_faite == False:
                if pokemon.PV < pokemon.stats[0]/2: # si le Pokémon a moins de la moitié de ses PV
                    if pokemon == "utile" and option1[0] == True: # si le Pokémon est encore utile, à définir
                        action_faite = self.utiliser_objet("PV")
                        option1[0] = action_faite
                    elif option1[1] == True:
                        liste = []
                        for pokemon in self.equipes["ordi"]:
                            if pokemon.PV > 0 and not (self.pokemons_en_jeu["ordi"] == pokemon): # on ne peut pas remettre le Pokémon en jeu en jeu
                                liste.append(pokemon)
                        action_faite = self.choisir_pokemon_a_mettre_en_jeu_ordi(liste)
                        option1[1] = action_faite
                elif pokemon.est_desavantage_type(ennemi) and option2 == True:
                    action_faite = self.changer_pokemon()
                    option2 = action_faite
                elif pokemon.etat != None: # si le Pokémon a un problème de statut
                    if ((pokemon.etat == "Empoisonnement" and pokemon.role == "Tank") or pokemon.etat == "Empoisonnement grave") and option3[0] == True:
                        action_faite = self.utiliser_objet("Empoisonnement")
                        option3[0] = action_faite
                    elif pokemon.etat == "Brûlure" and pokemon.orientation == "Physique" and option3[1] == True:
                        action_faite = self.utiliser_objet("Brûlure")
                        option3[1] = action_faite
                    elif pokemon.etat == "Paralysie" and pokemon.role == "Sweeper" and option3[2] == True:
                        action_faite = self.utiliser_objet("Paralysie")
                        option3[2] = action_faite
                    elif pokemon.etat == "Sommeil" and option3[3] == True:
                        action_faite = self.utiliser_objet("Sommeil")
                        option3[3] = action_faite
                    elif pokemon.etat == "Gel" and option3[4] == True:
                        action_faite = self.utiliser_objet("Gel")
                        option3[4] = action_faite
                elif ennemi.PV < ennemi.stats[0]/7 and option4 == True: # si l'ennemi n'a plus que environ 15% de ses PV
                    pass # ATTAQUER AVEC UNE ATTAQUE PRIORITAIRE
                    # option4 = action_faite
                elif ennemi.role == "tank" and option5 == True:
                    pass # ATTAQUER AVEC UNE ALTÉRATION DE STATUT
                    # option5 = action faite
                else:
                    pass # attaquer ou booster les stats
                    # action_faite = True ou False

    

    def getPokemonParNom(self, nom:str):
        for p in self.equipes["ordi"]:
            if p.getNom().lower() == nom.lower():
                return p
        return None
    
    def choisir_action_IA(self, pokemon_actuel, type_attaque_recue):
        """
        Choisit l'action à effectuer au prochain tour pour l'IA
        en fonction du type d'attaque subie et du Pokémon actuellement en jeu.
        L'action est stockée dans self.action_retardee["ordi"] pour exécution au tour suivant.
        """
    
        nom_pokemon = pokemon_actuel.getNom().lower()
    
        # Cas 1 : Carchacrok
        if nom_pokemon == "carchacrok":
            if type_attaque_recue == "dragon":
                self.action_retardee["ordi"] = {"action": "attaquer", "capacite": "dracogriffe"}
                return
    
            elif type_attaque_recue == "poison":
                self.action_retardee["ordi"] = {"action": "attaquer", "capacite": "séisme"}
                return
    
            elif type_attaque_recue == "glace":
                millobelus = self.getPokemonParNom("millobelus")
                if millobelus and not millobelus.estKO():
                    self.action_retardee["ordi"] = {
                        "action": "switch",
                        "nouveau_pokemon": millobelus,
                        "attaque_prochaine": "ébullition"
                    }
                    return
    
        # Cas 2 : Milobellus
        elif nom_pokemon == "millobelus":
            if type_attaque_recue == "plante":
                roserade = self.getPokemonParNom("roserade")
                if roserade and not roserade.estKO():
                    self.action_retardee["ordi"] = {
                        "action": "switch",
                        "nouveau_pokemon": roserade,
                        "attaque_prochaine": "bombe beurk"
                    }
                    return
    
            elif type_attaque_recue == "electrique":
                carchacrok = self.getPokemonParNom("carchacrok")
                if carchacrok and not carchacrok.estKO():
                    self.action_retardee["ordi"] = {
                        "action": "switch",
                        "nouveau_pokemon": carchacrok,
                        "attaque_prochaine": "séisme"
                    }
                    return
    
        # Cas 3 : Roserade
        elif nom_pokemon == "roserade":
            if type_attaque_recue in ["feu", "glace"]:
                millobelus = self.getPokemonParNom("millobelus")
                if millobelus and not millobelus.estKO():
                    self.action_retardee["ordi"] = {
                        "action": "switch",
                        "nouveau_pokemon": millobelus,
                        "attaque_prochaine": "ébullition"
                    }
                    return
    
            elif type_attaque_recue == "vol":
                millobelus = self.getPokemonParNom("millobelus")
                if millobelus and not millobelus.estKO():
                    self.action_retardee["ordi"] = {
                        "action": "switch",
                        "nouveau_pokemon": millobelus,
                        "attaque_prochaine": "rayon glace"
                    }
                    return
    
        # Si aucun cas spécial, attaque aléatoire
        capacites_disponibles = pokemon_actuel.getCapacites()
        if capacites_disponibles:
            capacite_choisie = random.choice(capacites_disponibles)
            self.action_retardee["ordi"] = {"action": "attaquer", "capacite": capacite_choisie}
        else:
            # Fallback : attaque par défaut si aucune capacité trouvée
            self.action_retardee["ordi"] = {"action": "attaquer", "capacite": "charge"}


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
        nb = {"joueur":random.randint(1, 3), "ordi": random.randint(1, 3)}
        self.player = "joueur"
        if nb["joueur"] == 1:
            print("Vous obtenez une Baie Sitrus")
        elif nb["joueur"] == 2:
            print("Vous obtenez des Restes")
        else:
            print("Vous obtenez un Casque Brut")
        for i in range(len(self.equipes["joueur"])):
            print(i+1, ". ", self.equipes["joueur"][i])
        choix = {"joueur": self.choisir_nombre("Choisissez le Pokémon à qui vous voulez donner cet objet", 1, len(self.equipes["joueur"]))}

        self.player = "ordi"
        nb_2 = random.randint(1, len(self.equipes["ordi"]))
        for i in range(len(self.equipes["ordi"])):
            if i == nb_2:
                choix["ordi"] = self.equipes["ordi"][i]

        for player in ["joueur", "ordi"]:
            self.player = player
            if nb[player] == 1:
                choix[player].objet_tenu = Objets("Baie Sitrus")
            elif nb[player] == 2:
                choix[player].objet_tenu = Objets("Restes")
            else:
                choix[player].objet_tenu = Objets("Casque Brut")

        while self.verifier_victoire == None:
            self.player = "joueur"
            action_joueur = self.choisir_option_joueur()
            self.player = "ordi"
            action_ordi = self.choisir_option_ordi()
            
            if action_ordi[0] == 3 or action_joueur[0] == 3:
                if action_ordi[0] == action_joueur[0]: # si les deux changent de Pokémon, on calcule la priorité
                    if action_ordi[1].stats[5] == action_joueur[1].stats[5]:
                        if random.randint(1, 2) == 1:
                            self.player = "ordi"
                            self.changer_pokemon(action_ordi[1], "ordi")
                        else:
                            self.player = "joueur"
                            self.changer_pokemon(action_joueur[1], "joueur")
                    elif action_ordi[1].stats[5] < action_joueur[1].stats[5]:
                        self.player = "joueur"
                        self.changer_pokemon(action_joueur[1], "joueur")
                    else:
                        self.player = "ordi"
                        self.changer_pokemon(action_ordi[1], "ordi")
                else: 
                    if action_joueur[0] == 3:
                        self.player = "joueur"
                        self.changer_pokemon(action_joueur[1], "joueur")
                    else:
                        self.player = "ordi"
                        self.changer_pokemon(action_ordi[1], "ordi")
            
            if action_ordi[0] == 2 or action_joueur[0] == 2:
                if (action_joueur[0] == action_ordi[0] and random.randint(1, 2) == 1) or action_joueur[0] == 2:
                    if random.randint(1, 2) == 1:
                        self.player = "joueur"
                        self.utiliser_objet(action_joueur[1])
                else:
                    self.player = "ordi"
                    self.utiliser_objet(action_ordi[1])

            if action_ordi[0] == 1 or action_joueur[0] == 1:
                if action_ordi[1].priorite > action_joueur[1].priorite:
                    self.player = "ordi"
                    action_ordi[1].utiliser_capacite()
                elif action_ordi[1].priorite < action_joueur[1].priorite:
                    self.player = "joueur"
                    action_joueur[1].utiliser_capacite()
                elif self.pokemons_en_jeu["ordi"].stats[5] > self.pokemons_en_jeu["joueur"].stats[5]:
                    self.player = "ordi"
                    action_ordi[1].utiliser_capacite()
                else:
                    self.player = "joueur"
                    action_joueur[1].utiliser_capacite()

            for player in ["ordi", "joueur"]:
                if self.pokemons_en_jeu[player].objet_tenu != None:
                    self.player = player
                    if self.pokemons_en_jeu[player].objet_tenu.nom == "Baie Sitrus" and self.pokemons_en_jeu[player].PV < self.pokemons_en_jeu[player].stats[0]/2:
                        self.pokemons_en_jeu[player].objet_tenu.utiliser_objet_tenu(self.pokemons_en_jeu[player])
                    elif self.pokemons_en_jeu[player].objet_tenu.nom == "Restes":
                        self.pokemons_en_jeu[player].objet_tenu.utiliser_objet_tenu(self.pokemons_en_jeu[player])
            
        if self.verifier_victoire == "égalité":
            print("Il y a eu égalité")
        elif self.verifier_victoire == "joueur":
            print("Le joueur a gagné")
        else:
            print("L'ordinateur a gagné")




def appliquer_effets_statuts(self):
    for joueur in ["joueur", "ordi"]:
        pokemn = self.pokemons_en_jeu[joueur]
        statut = pokemn.statut

        if statut is None:
            continue

        effets = STATUTS[statut]

        if effets["effet"] == "pv_perte":
            perte = int(pokemn.stats[0] * effets["valeur"])
            pokemn.PV -= perte
            print(f"{pkmn.nom} souffre de {statut.lower()} et perd {perte} PV !")
            if pokemn.PV < 0:
                pokemn.PV = 0

        elif effets["effet"] == "chance_inactif":
            pass  # traité au moment d'attaquer

        elif effets["effet"] == "inactif":
            pokemn.statut_duree -= 1
            if pokemn.statut_duree <= 0:
                print(f"{pokemn.nom} se réveille !")
                pokemn.statut = None

        elif effets["effet"] == "inactif_prob":
            if random.random() < effets["probabilite"]:
                print(f"{pokemn.nom} se dégèle !")
                pokemn.statut = None

        
class Objets:
    def __init__(self, nom, objet_type=None, info=None):
        self.nom = nom
        self.objet_type = objet_type
        self.info = info # nombre de PV pour les soins, cas où l'utiliser pour les sprays de statut
        self.quantite = 0

    def utiliser_objet_tenu(self, pokemon:Pokemon):
        if self.nom == "Restes":
            pokemon.PV += pokemon.stats[0]/16 # avec Restes, récupère 1/16 de ses PV chaque tour (ne pert pas l'objet)
        elif self.nom == "Baie Sitrus":
            pokemon.PV += pokemon.stats[0]/4 # avec Baie Sitrus, récupère 1/4 de ses PV (pert l'objet)
            pokemon.objet_tenu = None

        if pokemon.PV > pokemon.stats[0]:
            pokemon.PV = pokemon.stats[0] # pour pas avoir plus de PV que ceux de base

    def utiliser_objet(self):
        """
        Retire l'objet utilisé de la liste des objets et effectue l'action liée à cet objet
        """
        for i in range(len(combat.listes_objet[combat.player])):
            if combat.listes_objet[combat.player][i][0] == self.nom: 
                combat.listes_objet[combat.player][i][2] -= 1 # On retire 1 à la quantité de l'objet
                if combat.listes_objet[combat.player][i][2] <= 0:
                    del combat.listes_objet[combat.player][i] # si c'était le dernier exemplaire de cet objet, on le supprime complètement
        combat.listes_objet[combat.player][1].quantite -= 1

        if self.objet_type == "Soins":
            pokemon_choisi = combat.choisir_pokemon()
            if self.info == "max":
                PV_a_rajouter = pokemon_choisi.stats[0]
            else:
                PV_a_rajouter = self.info
            
            PV_max_a_rajouter = pokemon_choisi.stats[0] - pokemon_choisi.PV # calcule le nombre max de PV qu'on peut rajouter au Pokémon
            if PV_a_rajouter >= PV_max_a_rajouter:
                pokemon_choisi.PV = pokemon_choisi.stats[0]
            else:
                pokemon_choisi.PV += PV_a_rajouter

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
                        print("Ce Pokémon n'est pas KO, merci d'en choisir un autre qui l'est")
            
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

# Création des capacités : nom, type, classe, PP, probabilité, puissance, priorité , statut, chance_statut
detricanon = Capacite("Détricanon", "Poison", "Physique", 5, 80, 120, 1)
repos = Capacite("Repos", "Psy", "Statut", 5, 0, 0, 1, statut="Endormi", statut_chance=1)
bombe_beurk = Capacite("Bombe Beurk", "Poison", "Spéciale", 10, 100, 90, 1, statut="Empoisonné", statut_chance=0.3)
seisme = Capacite("Séisme", "Sol", "Physique", 10, 100, 100, 1)
ebullition = Capacite("Ébullition","Eau","Spéciale", 15, 80, 100, 1, statut="Brûlé", statut_chance=0.5)
seisme = Capacite("Séisme","Sol","Spéciale", 10,100,100,1)
# attention : pas défini
ball_ombre = Capacite()
eclat_magique = Capacite("Éclat Magique","Fée","Spéciale",16,80,100,1)
eco_sphere=Capacite("Éco-Sphère","Plante","Spéciale",10,90,100,1)
soin=Capacite("Soin","Normal","Statut",5,0,0,1)
voile_miroir= Capacite("Voile Miroir","Psy","Statut",20,0,100,1)
laser_glace = Capacite("Laser Glace","Glace","Spéciale",10,90,100,1, statut="Gelé", statut_chance=0.3)

#nouveau
# Dictionnaire nom -> objet Capacite
CAPACITES = {
    "Détricanon": detricanon,
    "Repos": repos,
    "Bombe Beurk": bombe_beurk,
    "Séisme": seisme,
    
}

#nouveau
#effet de statut et conséquence
STATUTS = {
    "Brûlure": {
        "effet": "pv_perte",
        "valeur": 1/16,  # perte de 1/16 PV max par tour
        "attaque_divisee": True  # baisse attaque
    },
    "Paralysie": {
        "effet": "chance_inactif",
        "probabilite": 0.25,  # 25 % de chance de ne pas agir
        "vitesse_divisee": True  # baisse vitesse
    },
    "Sommeil": {
        "effet": "inactif",
        "duree_min": 1,
        "duree_max": 3
    },
    "Gel": {
        "effet": "inactif_proba",
        "probabilite": 0.2  # 20% de chance de se dégeler par tour
    },
    "Poison": {
        "effet": "pv_perte",
        "valeur": 1/8
    }
}

# pour les EV et les stats : [HP, Attaque, Défense, Attaque Spé, Défense Spé, Vitesse]
roserade = Pokemon("Roserade", ["Plante","Poison"], 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
carchacrok = Pokemon("Carchacrok", ["Dragon" , "Sol"], 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
milobellus = Pokemon("Milobellus", "Eau", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
dracolosse = Pokemon("Dracolosse", ["Dragon" "Vol"], 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout5 = Pokemon("Brindibou", "Plante", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})
avaltout6 = Pokemon("Avaltout", "Poison", 50, [100, 73, 83, 73, 83, 55], [207, 125, 135, 125, 135, 107], capacites_noms(["Detricanon", "Repos", "Bombe Beurk", "Séisme"]), {"Sol": 2, "Psy": 2, "Insecte": 0.5, "Plante": 0.5, "Fée": 0.5, "Combat": 0.5, "Poison": 0.5})

combat = Combat(roserade, carchacrok, [roserade, milobellus, avaltout5], [carchacrok, dracolosse, avaltout6])
#objet = Objets("objet", "joueur")
