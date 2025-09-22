Chloé:
- J'ai ajouté une methode choisir_action_IA qui choisi un peu plus specifiquement ce que les pokemon de l'IA vont faire selon les types des capacites.(et aussi eviter de melanger avec ton IA que tu a creer si jamais ce que j'ecrit ne fonctionne pas au final)
- il y a l'attribut action_retarde: dict dans class combat pour ma methode.
- j'ai aussi fait un dictionnaire au final pour les capacites et une methode aussi parce que ça ne marchait pas pour ma methode choisir_action_IA sans ça.
- les effets de statuts je les mettrait a jour pendant la pause dejeuner de mardi







# Combats-Pokemon

infos : 
- j'ai rassemblé les baisser_attaque et monter_attaquer (et pareil pour les PV et la défense), car on peut juste mettre un nombre négatif en entrée pour que ça fasse baisser le nombre d'attaque/défense/PV donc ça revient au même normalement
- je n'ai pas compris ce que tu as fait dans la méthode attaquer, avec len(attaque) == 3 ? donc j'ai laissé comme ça mais ça ne fonctionne probablement pas
    --> je sais juste que "attaquant", c'est censé être : self.pokemons_en_jeu[self.player]
    --> et "cible" je l'ai défini juste avant pour que ça fonctionne
- j'ai remis la classe Error parce qu'en fait tu l'appelais quelque part

Objets :
⦁	Soins
    ⦁	Potion : 20 PV
    ⦁	Super Potion : 50 PV
    ⦁	Hyper Potion : 200 PV
    ⦁	Potion Max : tous les PV
⦁	PPS
    ⦁	Huile : 10 PP d'une capacité
    ⦁	Huile Max : tous les PP d'une capacité
    ⦁	Elixir : 10 PP de toutes les capacités
    ⦁	Elixir Max : tous les PP de toutes les capacités
⦁	Réanimation
    ⦁	Rappel : ramine un pokémon KO + la moitié de ses PV
    ⦁  	Rappel Max : ramine un pokémon KO + tous ses PV
    ⦁	Cendre sacrée : ranime tous les pokémon KO + tous leurs PV
⦁	Statut
    ⦁	Total soin : soigne tous les problèmes de statut
    ⦁	Anti-Para : soigne la paralysie
    ⦁	Anti-Brûle : soigne les brûlures
    ⦁	Antigel : réchauffe le pokémon gelé
    ⦁	Antidote : guérit d'un empoisonnement
    ⦁	Réveil : réveille un pokémon endormi
⦁	Autres
    ⦁	Guérison : tous les PV + soigne tous les problèmes de statut
