#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LibreOffice Controller
application.py
======================
Serveur de contrôle d'un diaporama Libre Office.
:platform: Linux
:copyright: (c) 2017 Ville de Nevers
:license: GNU GPLv3, ouvrir LICENSE pour plus d'information.
:author: Romain B. <rb@ville-nevers.fr>
"""

import configparser
import logging
import os
import subprocess

from logging.handlers import RotatingFileHandler
from robotListener import RobotListener


class Application(object):

    def __init__(self):

        self.server = None

        # Recuperation Propriete

        self.properties = configparser.ConfigParser()
        try:
            self.properties.read_file(open(os.path.dirname(os.path.abspath(__file__)) + "/config/config.properties"))
        except:
            self.logger.fatal("Impossible d'ouvrir le fichier de configuration.")

        #Initialisation logger
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        logFormatter = logging.Formatter('%(asctime)s :: [%(levelname)s] :: %(message)s')

        fileHandler = RotatingFileHandler(self.properties["SERVER"]["server.logFile"], 'a', 2000000, 1)
        fileHandler.setFormatter(logFormatter)

        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(logFormatter)

        self.logger.addHandler(fileHandler)
        self.logger.addHandler(streamHandler)



        ### Build UI ###

        # Fenetre
        self.window = Tk()
        self.window.title("LibreOffice Impress Controller.")
        self.window.resizable(width=False,height=False)
        self.window.geometry("500x70+100+100")
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Widget
        self.restartButton = Button(self.window, text="Redémarrer le serveur de diffusion", command=self.restart_service)
        self.logButton = Button(self.window, text="Afficher les logs", command=self.show_logs)
        self.quitButton = Button(self.window, text="Quitter", command=self.on_closing)

        # Position Widget
        self.restartButton.grid(row=0,column=1,padx=(10,5),pady=20)
        self.logButton.grid(row=0,column=2,padx=(5,5),pady=20)
        self.quitButton.grid(row=0,column=3,padx=(20, 10),pady=20,sticky=E)

        self.logger.info("Lancement du programme.")
        self.start_service()
        self.window.mainloop()

    # REDEMARRAGE DU SERVICE LIBRE OFFICE ET DU LISTENER
    def restart_service(self):
        if(type(self.server) != None):
            self.stop_service()
        self.start_service()


    # DEMARRAGE DE LIBRE OFFICE ET DU LISTENER
    def start_service(self):

        try:
            self.logger.info("Démarrage de libre office.")
            process = os.popen(self.properties["SOFFICE"]["soffice.bin"] + " --show " + self.properties["SOFFICE"]["soffice.file"])
        except:
            self.logger.error("Une erreur est survenue pendant le démarrage de libre office.")

        try:
            self.logger.info("Démarrage du listener.")
            self.server = RobotListener()
            self.server.start()
        except:
           self.logger.error("Une erreur est survenue pendant le démarrage du listener.")

    # ARRET DE LIBRE OFFICE ET DU LISTENER
    def stop_service(self):

        try:
            self.logger.info("Arrêt du listener.")
            self.server.stop()
        except:
            self.logger.error("Une erreur est survenue pendant l'arrêt du listener.")

        try:
            self.logger.info("Arrêt du processus libre office.")
            subprocess.check_output("killall -q soffice.bin", shell=True)
        except subprocess.CalledProcessError as e:
            self.logger.debug(e)

    # AFFICHAGE DES LOGS DEPUIS L'EDITEUR LOCAL
    def show_logs(self):
        try:
            subprocess.Popen([self.properties["SERVER"]["server.logEditor"],"--new-window",self.properties["SERVER"]["server.logFile"]])
        except:
            self.logger.error("Une erreur est survenue pendant l'ouverture du programme de lecture des logs.")

    # FERMETURE DE LA FENETRE ET DU PROGRAMME
    def on_closing(self):
        self.stop_service()
        self.window.destroy()


if __name__ == '__main__':
    from tkinter import *
    window = Application()





