# Card Crawl

Ce projet a été réalisé dans le cadre de l'UE "Programmation" de la L3 MIASHS. Il consiste à développer un programme en Crawl qui implémente une variante du jeu Card Crawl disponible sur les smartphones Android et iOS, ainsi que sur Steam. Le jeu appartient à la famille des rogue-like games où le joueur incarne un aventurier explorant un donjon rempli de monstres et de trésors, avec pour objectif de sortir vivant du donjon tout en éliminant tous les monstres et en collectant un maximum de richesses.

## Description

La particularité de cette variante est que le jeu se joue intégralement avec des cartes, réparties en 6 catégories : monstres, pièces d'or, épées, boucliers et potions de guérison. Chaque pièce du donjon est représentée par un ensemble de 4 cartes distribuées dans la zone de jeu. Le joueur doit récupérer les cartes d'or ou d'équipement et combattre les monstres. Le joueur ne possède que 3 emplacements pour stocker son équipement (main gauche, main droite et sac à dos) et ne peut passer à la pièce suivante tant qu'il reste plus d'une carte dans la zone de jeu.

## Interface du jeu

L'interaction entre le programme et le joueur s'effectue uniquement à l'aide de la souris. L'interface du jeu comporte une grille de cartes représentant les différentes pièces du donjon, ainsi que des emplacements pour l'équipement du joueur.

<p align="center">
  <img width="550" alt="Interface du jeu" src="https://github.com/alexandra002/cardcrawl/assets/108056034/64e4a64f-34fe-40d5-bc35-f62dea6bdebb">
</p>

## Méthodologie

Le développement du jeu s'est déroulé en plusieurs étapes :

- Modélisation du jeu : Définition des règles du jeu et des différentes classes pour représenter le donjon, les cartes, et l'équipement du joueur.
  
- Implémentation de l'interface graphique : Création de la fenêtre graphique pour visualiser le plateau de jeu et gestion des actions du joueur.

- Développement des fonctionnalités de jeu : Ajout des fonctionnalités pour le déroulement du jeu, telles que la gestion des cartes, des combats avec les monstres, la collecte de trésors, etc.

## Accès au code et aux ressources

Le code source du programme est disponible dans ce dépôt GitHub. Vous pouvez également accéder aux ressources nécessaires pour l'interface graphique, telles que les images des cartes et des zones vides du plateau de jeu.

