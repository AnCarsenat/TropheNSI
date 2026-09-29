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
- Permettre a chaque type de node de definir des proprietes supplementaires et
	typees. Par exemple, `Sprite2D` doit pouvoir exposer `properties.image` et accepter
	directement le chemin du fichier image.
- Conserver dans les scenes un chemin logique portable, avec `/` comme separateur et
	un chemin relatif a la racine du projet. Ne jamais stocker un chemin absolu propre a
	Windows, Linux ou macOS dans une scene.
- Resoudre ce chemin avec `pathlib.Path` selon l'OS courant, verifier qu'il reste dans
	la racine du projet, puis charger la ressource au moment necessaire. Le node conserve
	le chemin logique ; le renderer recoit une ressource chargee ou un handle independant
	du systeme de fichiers.
	Exemple :

```python
class Sprite2D(Node2D):
    def __init__(self, image=None, **kwargs):
        super().__init__(**kwargs)
        self.properties.image = image

sprite = Sprite2D(image="resources/images/my_sprite.png")
```

- Ajouter `add_child()` et `remove_child()` pour maintenir automatiquement les liens
	parent/enfant et refuser les arbres invalides.
- Utiliser la position locale d'un noeud et calculer sa position globale a partir de
	ses parents.

**Validation :** tester l'ajout, le retrait, les parents invalides et le calcul de la
position globale sur au moins deux niveaux de profondeur.

## 2. Validation de la boucle du jeu

- Tester `Game.tick(delta_time)` avec une scene et des faux noeuds qui enregistrent les
	appels.
- Verifier la valeur de `delta_time`, l'ordre de propagation et l'absence d'etat partage
	entre deux instances de `Game`.

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
	des interfaces separees : `Renderer` pour le dessin, `Window` pour la fenetre,
	`Input` pour le clavier et la souris, et `Audio` pour les sons et la musique.
- Permettre de remplacer Pygame par un autre backend sans modifier les scenes ni la
	logique des noeuds.
- Definir le pipeline de dessin d'une frame : mettre a jour les transformations globales,
	ignorer les noeuds invisibles, appliquer la camera, trier les noeuds selon leur ordre
	de rendu, convertir leurs proprietes en commandes de dessin, puis les transmettre au
	backend.
- Centraliser dans le renderer la conversion des positions, rotations, echelles,
	couleurs, textures et surfaces vers les primitives du backend.
- Definir un registre ou un gestionnaire de ressources capable de charger, typer,
	mettre en cache et fournir les ressources a partir d'un chemin de fichier (`.png`,
	`.jpg`, `.wav`, `.ttf`, etc.).
- Normaliser les separateurs, les chemins relatifs et les encodages sans modifier la
	valeur logique declaree dans la scene, afin qu'un meme projet fonctionne sur plusieurs
	systemes d'exploitation.
- Permettre a une scene de declarer une ressource d'image puis de l'affecter a la
	propriete `image` d'un `Sprite2D` avec un chemin direct, avec une erreur claire si le
	fichier est introuvable ou si son type est incompatible.
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

La racine d'un projet est le dossier contenant `main.py` ou `projet.yaml`. Tous les
chemins de ressources et de scenes sont relatifs a cette racine, quel que soit le
repertoire courant depuis lequel le projet est lance.

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
- Resoudre tous les chemins du projet relativement a sa racine et refuser les chemins
	qui sortent de ce dossier.
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

Le renderer est un backend interchangeable. Il ne doit recevoir que les commandes de
dessin du moteur. La fenetre, les evenements et l'audio peuvent provenir de bibliotheques
distinctes ; un projet choisit donc une combinaison de backends qui declare ses
capacites et libere correctement ses ressources.

- **Pygame 2 :** choix prioritaire pour le prototype ; fournit une fenetre, les
	evenements clavier/souris, le rendu 2D, les images et l'audio via SDL2. Les touches
	doivent etre converties en evenements generiques `Input`.
- **PySDL2 :** acces direct a SDL2 ; `SDL_Event` fournit les evenements clavier et
	souris, tandis que `SDL_mixer` ou une couche audio SDL gere les sons et la musique.
	Le rendu peut utiliser SDL2 directement ou etre remplace par OpenGL.
- **pyglet :** gere fenetre, clavier, souris, audio et contexte OpenGL ; adapte a un
	renderer 2D accelere.
- **Arcade :** framework 2D construit autour de pyglet ; fournit deja des abstractions
	pour les sprites, les evenements et le son, mais impose davantage son architecture.
- **PyOpenGL ou ModernGL :** fournissent uniquement l'acces au rendu OpenGL. Ils ne
	recuperent pas les touches et ne jouent pas les sons seuls : les evenements doivent
	venir d'une fenetre SDL2, GLFW, pyglet ou equivalente, et l'audio d'un module comme
	SDL_mixer, pyglet ou pygame.mixer.
- **Tkinter Canvas :** fournit le dessin et les evenements via `bind()` ; il faut une
	bibliotheque separee pour l'audio, et les transformations sont limitees.
- **cairo ou pycairo :** fournit le rendu vectoriel, mais ni fenetre, ni clavier,
	souris, ni audio. Il doit etre combine avec Tkinter, SDL2 ou une autre couche.
- **Terminal ASCII ou backend headless :** peut recevoir des entrees terminal ou des
	evenements simules pour les tests ; il ne fournit pas de sortie audio par defaut.

Combinaisons recommandees :

- `Pygame 2` pour un jeu 2D simple avec fenetre, input, audio et rendu reunis ;
- `PySDL2 + ModernGL` pour le rendu OpenGL avec fenetre, clavier, souris et audio SDL2 ;
- `pyglet` seul pour une solution OpenGL/2D disposant deja de l'input et de l'audio ;
- `cairo + Tkinter` pour un outil 2D ou un editeur, avec une bibliotheque audio ajoutee
	seulement si necessaire.

Le premier backend a implementer est Pygame. Les autres restent des extensions possibles
tant qu'ils respectent les interfaces `Renderer`, `Input` et `Audio` sans contaminer le
coeur du moteur.

**Validation :** lancer un projet avec `main.py` seul, lancer un projet avec manifeste,
charger une scene explicitement depuis un autre repertoire courant et verifier qu'un
backend headless permet de tester la logique sans ouvrir de fenetre.

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