#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LibreOffice Controller
robotListener.py
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
import socket

from impressController import ImpressController
from logging.handlers import RotatingFileHandler
from threading import Thread


class RobotListener(Thread):
    """Gere la communication avec le robot
    Un objet RobotListener recoit les requetes depuis un socket
    et instancie un nouveau thread ImpressController pour les traiter
    """

    def __init__(self):
        Thread.__init__(self)

        # Init logger
        self.logger = logging.getLogger()

        # Champs
        self.listen = 1
        self.listener_socket = None

        # Get Properties
        self.properties = configparser.ConfigParser()
        try:
            self.properties.read_file(open(os.path.dirname(os.path.abspath(__file__)) + "/config/config.properties"))
        except:
            self.logger.fatal("Impossible d'ouvrir le fichier de configuration.")

    # DEMARRAGE DU THREAD
    def run(self):

        buffer_size = 20

        self.listener_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listener_socket.bind((self.properties["SERVER"]["server.ip"], self.properties["SERVER"].getint("server.port")))
        self.listener_socket.listen(5)

        while(self.listen == 1):

            try:
                client, address = self.listener_socket.accept()
                response = client.recv(buffer_size)
                self.logger.info("reception d'une requête depuis {} ".format( address ) + " ["+ response.decode("utf-8") +"]")

                if response != "":
                    impressThread = ImpressController(response)
                    impressThread.start()
                    impressThread.join()
                    self.logger.debug("Thread terminé.")
            except:
                self.logger.warning("Listener arrêté.")

    # ARRET DU THREAD
    def stop(self):
        self.logger.info("Arrêt du listener.")
        self.listener_socket.shutdown(socket.SHUT_RDWR)
        self.listen = 0
