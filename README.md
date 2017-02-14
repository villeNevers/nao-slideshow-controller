# VILLE DE NEVERS - CONTROLE DE DIAPORAMA LIBRE OFFICE POUR NAO / PEPPER #

Cette application a été développée par la Ville de Nevers dans le cadre d'un projet robotique avec [Nao](https://www.ald.softbankrobotics.com/en/cool-robots/nao "Nao").

Elle permet au robot de contrôler un diaporama diffusé sur un poste distant.

Les développements ont été réalisés en Python.

---

## Poste de diffusion ##

**Attention : l'application de gestion du serveur de diffusion ne fonctionne pour l'instant que sous Linux.**

*Pour fonctionner sous Windows, des adaptations doivent être apportées, notamment au niveau de la gestion de l'interface graphique avec TKinter.*


* version de Python : 3.x (livrée avec Libre Office)
* version de Libre Office : 5.x

Le programme se base sur la version de Python intégrée à Libre Office. Elle contient la librarie UNO.

### Usage ###

1. Copier le contenu du dossier "serveur" sur le poste de diffusion
2. Modifier le fichier de configuration pour s'adapter à votre environnement
3. Configurer Libre Office pour accepter le contrôle distant (Outils >> Libre Office Impress >> Général >> Activer le contrôle à distance)
4. Lancer le programme en ligne de commande avec la version de python associée à Libre Office

Au besoin, vous pouvez automatiser le lancement du programme au démarrage.

Un exemple de script pour épurer les logs est aussi fourni. Il peut être intégré à une tâche cron. 

### Fonctionnement ###

Le programme lance automatiquement Libre Office Impress (en lecture seule) avec le diaporama spécifié en paramètre. 

Le redémarrage supprime les instances en cours d'execution pour en relancer une nouvelle.

---

## Robot Nao ##

* version de python : 2.7

### Usage ###

La librairie TVCast.py doit être intégrée à votre projet sous Chorégraphe.

Des exemples de scripts pour Box Choregraphe sont fournis. 