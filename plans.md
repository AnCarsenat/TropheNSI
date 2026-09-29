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

## Chargement et threads

- Garder la logique de gameplay et la propagation des noeuds sur le thread principal.
- Utiliser les threads pour les chargements de fichiers, le decodage des ressources et les autres operations d'I/O independantes.
- Appliquer les resultats d'un chargement a la scene sur le thread principal.