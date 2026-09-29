# Feuille de route

Ce document decrit les prochaines evolutions du moteur et les criteres permettant de
considerer chaque etape comme terminee. Les changements doivent rester compatibles
avec l'architecture actuelle et etre accompagnes de tests.

## Priorites

1. Stabiliser l'architecture des noeuds et la boucle du jeu.
2. Ajouter les scenes chargeables, les scripts et les mecanismes de communication.
3. Construire la couche de rendu et d'I/O autour du coeur du jeu.
4. Automatiser les tests, l'installation et la distribution.

## 1. Architecture de la scene

- Garder dans `Node2D.Properties` les donnees du noeud : position locale, rotation,
	echelle, visibilite et options de rendu.
- Ajouter `add_child()` et `remove_child()` pour maintenir automatiquement les liens
	parent/enfant et refuser les arbres invalides.
- Utiliser la position locale d'un noeud et calculer sa position globale a partir de
	ses parents.

**Validation :** tester l'ajout, le retrait, les parents invalides et le calcul de la
position globale sur au moins deux niveaux de profondeur.

## 2. Boucle du jeu

**Validation :** utiliser un faux noeud qui enregistre les appels et verifier la valeur
de `delta_time`, l'ordre de propagation et l'absence d'etat partage entre deux jeux.

## 3. Scenes, scripts et communication

- Definir un format textuel de scene inspire de Godot (`.tscn`) pour decrire l'arbre,
	les proprietes, les ressources et les scripts attaches.
- Charger une scene depuis un fichier, reconstruire ses noeuds et valider les types et
	proprietes avant son integration dans `Game`.
- Definir les chemins de noeuds suivants : relatif (`../Enemy`), absolu depuis la
	racine (`/root/Player`) et raccourci vers la racine (`$Player`).
- Centraliser leur resolution dans `Node2D.get_node(path)` et ajouter `has_node(path)`
	pour tester un chemin sans lever d'erreur.
- Ajouter un systeme de signaux : declaration, connexion, emission avec arguments et
	deconnexion propre lors de la destruction d'un noeud.
- Permettre d'attacher un script Python depuis le fichier de scene, avec les points
	d'entree `_ready`, `tick` et `on_destroy`.
- Donner a chaque script une reference vers son noeud (`self.node`) et le contexte du
	jeu (`self.game`), sans imposer d'heriter de `Game`.
- Faire communiquer les scripts principalement par signaux et chemins de noeuds pour
	limiter leurs dependances directes.
- Documenter l'ordre du cycle de vie : creation, ajout a la scene, `_ready`, `tick`,
	retrait et `on_destroy`. Preciser aussi les regles de rechargement des scripts.

**Validation :** ajouter une scene minimale chargeable, tester les trois formes de
chemin, puis verifier qu'un signal connecte et deconnecte respecte le cycle de vie.

## 4. Chargement et threads

- Garder la logique de gameplay et la propagation des noeuds sur le thread principal.
- Utiliser les threads uniquement pour les chargements de fichiers, le decodage des
	ressources et les autres operations d'I/O independantes.
- Appliquer les resultats d'un chargement a la scene sur le thread principal.
- Definir le comportement en cas d'erreur, d'annulation et de chargements termines
	dans un ordre different de celui des demandes.

**Validation :** simuler un chargement lent et verifier qu'aucun noeud n'est modifie
depuis le thread secondaire.

## 5. Rendu et integration de Pygame

- Connecter le moteur a Pygame via un wrapper qui centralise la fenetre, les evenements,
	le rendu, l'horloge et l'arret propre.
- Garder les classes du coeur independantes de Pygame autant que possible.
- Convertir les proprietes de rendu de `Node2D` en operations Pygame previsibles.
- Ajouter au minimum la gestion de la taille de fenetre, du plein ecran, du redimensionnement,
	de la fermeture et du taux de rafraichissement.

**Validation :** lancer une scene contenant un noeud visible, traiter la fermeture de la
fenetre et verifier que le coeur reste testable sans affichage graphique.

## 6. Qualite, distribution et documentation

- Ecrire des tests pour les classes et fonctions publiques de chaque module, en donnant
	la priorite aux mathematiques, a l'arbre de scene et a la boucle du jeu.
- Ajouter des tests d'integration pour le chargement d'une scene et le wrapper Pygame.
- Documenter dans `README.md` l'installation, le lancement, les tests et les versions
	de Python supportees.
- Ajouter Docker pour obtenir un environnement reproductible et documenter la commande
	de lancement.
- Definir une procedure de compilation ou de distribution du jeu, puis tester l'artefact
	produit sur un environnement propre.

**Definition de termine :** les tests passent, le projet se lance depuis une installation
propre, une scene minimale est chargee et affichee, et les limites connues sont documentees.