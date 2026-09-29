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
- Garder les classes du coeur independantes de Pygame autant que possible en definissant
	une interface de backend (`Renderer`, `Window` et gestionnaire d'evenements).
- Permettre de remplacer Pygame par un autre backend sans modifier les scenes ni la
	logique des noeuds.
- Definir le pipeline de dessin d'une frame : mettre a jour les transformations globales,
	ignorer les noeuds invisibles, appliquer la camera, trier les noeuds selon leur ordre
	de rendu, convertir leurs proprietes en commandes de dessin, puis les transmettre au
	backend.
- Centraliser dans le renderer la conversion des positions, rotations, echelles,
	couleurs, textures et surfaces vers les primitives du backend.
- Definir un point d'extension de rendu pour chaque type de noeud dessinable, sans faire
	appel directement a Pygame depuis `Node2D`.
- Ajouter au minimum la gestion de la taille de fenetre, du plein ecran, du redimensionnement,
	de la fermeture et du taux de rafraichissement.
- Definir la gestion des ressources graphiques : chemin du fichier, chargement, cache,
	liberation et comportement lorsqu'une ressource est introuvable.

**Validation :** lancer une scene contenant un noeud visible, verifier qu'il est dessine
au bon endroit apres transformation et camera, traiter la fermeture de la fenetre, puis
executer les tests du coeur sans affichage graphique.

## 6. Format et lancement d'un projet

Un projet doit pouvoir etre lance depuis un simple `main.py` ou depuis un dossier plus
structure. Le moteur ne doit pas imposer l'utilisation d'un manifeste ni d'un format de
scene : le code du projet peut creer les noeuds, appeler `load_scene()` ou charger les
ressources de la maniere la plus adaptee au jeu.

### Modes de projet acceptes

- **Script unique :** un fichier `main.py` initialise `Game`, cree ou charge une scene,
	choisit un renderer et demarre la boucle principale.
- **Projet Python :** un dossier contient `main.py`, des modules Python, des ressources
	et eventuellement des scenes. Le point d'entree reste libre et peut organiser le
	chargement comme il le souhaite.
- **Projet decrit par manifeste :** un fichier `projet.yaml` decrit le titre, les
	ressources, le renderer et une scene d'entree. Ce mode facilite les outils, mais
	reste optionnel.

```text
mon_projet/
|-- main.py
|-- projet.yaml                 # optionnel
|-- scenes/
|   |-- main.tscn
|   `-- ...
|-- resources/
|   |-- images/
|   |-- sounds/
|   `-- ...
`-- scripts/
```

- Si plusieurs points d'entree sont possibles, utiliser `main.py` par defaut et
	permettre de choisir explicitement un autre fichier ou module.
- Si `projet.yaml` est present, il peut definir `title`, `version`, `entry_scene`, les
	options de fenetre, le renderer, les ressources et les options de debug.
- Resoudre les chemins du manifeste relativement au dossier du projet et refuser les
	chemins qui sortent de ce dossier.
- Valider le manifeste avant son utilisation, avec des erreurs indiquant le fichier et
	la propriete fautive.
- Ne jamais charger automatiquement une scene lorsque le projet est pilote par `main.py`:
	le projet decide lui-meme quand et comment appeler `load_scene()`.
- Permettre de lancer le projet, ses tests et son mode debug depuis le meme dossier.

Exemple minimal de `projet.yaml` :

```yaml
title: Mon jeu
version: 0.1.0
engine: "1"
entry_scene: scenes/main.tscn
renderer: pygame
window:
  width: 1280
  height: 720
  fullscreen: false
```

### Renderers envisageables

Le renderer est un backend interchangeable. Tous doivent recevoir les commandes de
dessin du moteur, gerer leur fenetre et leurs evenements, puis liberer leurs ressources
proprement.

- **Pygame 2 :** choix prioritaire pour le prototype ; fenetre, clavier, souris, images,
	sons et primitives 2D via SDL2.
- **PySDL2 :** acces plus direct a SDL2 ; utile si le wrapper doit exposer davantage de
	fonctionnalites natives qu'avec Pygame.
- **pyglet :** fenetre, evenements et OpenGL ; adapte a un renderer 2D accelere.
- **Arcade :** framework 2D construit autour de pyglet ; interessant pour les sprites,
	mais plus impose qu'un backend bas niveau.
- **PyOpenGL ou ModernGL :** rendu OpenGL personnalise ; puissant, mais necessite de
	gerer soi-meme les buffers, shaders, textures et conversions de coordonnees.
- **Tkinter Canvas :** rendu 2D simple pour des outils, editeurs ou prototypes, avec
	des performances et des transformations limitees.
- **cairo ou pycairo :** rendu vectoriel 2D et export vers des surfaces ou fichiers ;
	utile pour des interfaces et des images, moins adapte a une boucle de jeu complete.
- **Terminal ASCII ou backend headless :** rendu sans fenetre pour les tests, le debug,
	les serveurs et les environnements sans affichage.

Le premier backend a implementer est Pygame. Les autres restent des extensions possibles
tant qu'ils respectent la meme interface de renderer et ne contaminent pas le coeur du
moteur.

**Validation :** lancer un projet avec `main.py` seul, lancer un projet avec manifeste,
charger une scene explicitement et verifier qu'un backend headless permet de tester la
logique sans ouvrir de fenetre.

## 7. Qualite, distribution et documentation

- Ecrire des tests pour les classes et fonctions publiques de chaque module, en donnant
	la priorite aux mathematiques, a l'arbre de scene et a la boucle du jeu.
- Ajouter des tests d'integration pour le chargement d'un projet, d'une scene et du
	backend Pygame.
- Documenter dans `README.md` l'installation, le lancement, les tests et les versions
	de Python supportees.
- Ajouter Docker pour obtenir un environnement reproductible et documenter la commande
	de lancement.
- Definir une procedure de compilation ou de distribution du jeu, puis tester l'artefact
	produit sur un environnement propre.

**Definition de termine :** les tests passent, le projet se lance depuis une installation
propre, une scene minimale est chargee et affichee, et les limites connues sont documentees.