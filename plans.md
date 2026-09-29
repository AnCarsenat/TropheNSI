- Ecrire des tests pour chacune des classes et fonctions de chacun des modules
- Connecter avec pygame pour le dessin etc. (en faire un wrapper complet)
- Utiliser docker / compiler le jeu en plus

## Architecture de la scene

- Garder `parent` et `children` directement dans `Node2D` : ils representent la structure de l'arbre de scene.
- Garder dans `Node2D.Properties` les donnees du noeud : position locale, rotation, echelle, visibilite et options de rendu.
- Ajouter des methodes `add_child()` et `remove_child()` pour maintenir automatiquement les liens parent/enfant.
- Eviter `Vec2(0, 0)` comme valeur par defaut d'un argument ; utiliser `None` puis creer le vecteur dans le constructeur.
- Utiliser la position locale d'un noeud et calculer sa position globale a partir de ses parents.

## Boucle du jeu

- `Game` conserve le `delta_time` de la frame courante.
- `Game.tick(delta_time)` met a jour cette valeur, puis appelle `current_scene.tick()` sans transmettre `delta_time` a chaque noeud.
- La scene et ses noeuds doivent pouvoir acceder au contexte du jeu ou de la scene pour lire `delta_time` quand ils en ont besoin.
- Propager `tick()` aux enfants dans leur ordre d'ajout pour conserver un comportement deterministe.
- Utiliser `super().__init__()` dans les classes derivees comme `Scene2D`.
- Importer `Node2D` au runtime dans `scene2d.py` ; `TYPE_CHECKING` ne suffit pas pour une classe de base.
- Ne pas utiliser de variable globale pour `delta_time`, afin de faciliter les tests et de permettre plusieurs instances de jeu.

## Scenes, scripts et communication

- Ajouter un format de fichier de scene textuel inspire de Godot (`.tscn`) pour decrire l'arbre, les proprietes, les ressources et les scripts attaches.
- Permettre de charger une scene depuis un fichier, de reconstruire ses noeuds et de valider les types et proprietes avant son integration dans `Game`.
- Definir des chemins de noeuds de type Godot : chemin relatif (`../Enemy`), chemin absolu depuis la racine (`/root/Player`) et raccourci vers la racine (`$Player`) pour retrouver un noeud.
- Centraliser la resolution des chemins dans `Node2D.get_node(path)` et ajouter `has_node(path)` pour tester un chemin sans lever d'erreur.
- Ajouter un systeme de signaux : declaration de signaux, connexion d'un callback, emission avec arguments et deconnexion propre lors de la destruction d'un noeud.
- Permettre d'attacher un script Python a un noeud depuis le fichier de scene, avec des points d'entree previsibles (`_ready`, `tick` et `on_destroy`).
- Donner a chaque script une reference vers son noeud (`self.node`) et vers le contexte du jeu (`self.game`) sans imposer d'heriter de `Game`.
- Permettre aux scripts de communiquer principalement par signaux et chemins de noeuds ; limiter les dependances directes entre scripts pour conserver des scenes reutilisables.
- Definir les regles de cycle de vie, d'ordre d'execution et de rechargement des scripts attaches.

## Chargement et threads

- Garder la logique de gameplay et la propagation des noeuds sur le thread principal.
- Utiliser les threads pour les chargements de fichiers, le decodage des ressources et les autres operations d'I/O independantes.
- Appliquer les resultats d'un chargement a la scene sur le thread principal.