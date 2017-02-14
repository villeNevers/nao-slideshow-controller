#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
LibreOffice Controller
impressController.py
======================
Serveur de contrôle d'un diaporama Libre Office.
:platform: Linux
:copyright: (c) 2017 Ville de Nevers
:license: GNU GPLv3, ouvrir LICENSE pour plus d'information.
:author: Romain B. <rb@ville-nevers.fr>
"""

import logging
import uno

from logging.handlers import RotatingFileHandler
from threading import Thread


class ImpressController(Thread):
    # Variable de classe
    COMMAND_NEXT = "next"
    COMMAND_PREVIOUS = "previous"
    COMMAND_FIRST = "first"
    COMMAND_LAST = "last"
    COMMAND_SLIDE = "slide_"

    def __init__(self, command):
        Thread.__init__(self)

        # Init logger
        self.logger = logging.getLogger()

        # Get command to execute
        self.command = command.decode("utf-8")

        # Init Libre Office
        self.logger.info("Initialisation de Libre Office.")
        try:
            uno_context = uno.getComponentContext()
            uno_url_resolver = uno_context.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", uno_context)
            oo_context = uno_url_resolver.resolve("uno:socket,host=localhost,port=8100;urp;StarOffice.ComponentContext")
            service_manager = oo_context.ServiceManager
            desktop = service_manager.createInstanceWithContext("com.sun.star.frame.Desktop", oo_context)
            model = desktop.getCurrentComponent()
            presentation = model.Presentation
            self.impressController = presentation.getController()
        except:
            pass


    # DEMARRAGE DU THREAD
    def run(self):

        self.logger.info("Traitement de la requete recue.")

        try:
            if self.command.startswith(self.COMMAND_SLIDE):
                self.goto_slide(self.command.split("_")[1])
            else:
                processor = {self.COMMAND_FIRST   : self.goto_first_slide,
                             self.COMMAND_LAST    : self.goto_last_slide,
                             self.COMMAND_PREVIOUS: self.goto_previous_slide,
                             self.COMMAND_NEXT    : self.goto_next_slide,
                             }
                processor.get(self.command, self.unknown_command(self.command))()
        except:
            self.logger.error("Impossible de déterminer la requete.")

    # SLIDE PRECEDENT
    def goto_previous_slide(self):
        self.logger.info("Execution : <slide précédent>")
        try:
            self.impressController.gotoPreviousSlide()
        except:
            self.logger.error("Impossible d'executer la requête <slide précédent>")

    # SLIDE SUIVANT
    def goto_next_slide(self):
        self.logger.info("Execution : <slide suivant>")
        try:
            self.impressController.gotoNextSlide()
        except:
            self.logger.error("Impossible d'executer la requête <slide suivant>")

    # PREMIER SLIDE
    def goto_first_slide(self):
        self.logger.info("Execution : <first slide>")
        try:
            self.impressController.gotoFirstSlide()
        except:
            self.logger.error("Impossible d'executer la requête <first slide>")

    # DERNIER SLIDE
    def goto_last_slide(self):
        self.logger.info("Execution : <last slide>")
        try:
            self.impressController.gotoLastSlide()
        except:
            self.logger.error("Impossible d'executer la requête <last slide>")

    # ALLER AU SLIDE X
    def goto_slide(self, slide):
        self.logger.info("Execution : <slide n> " + slide)
        try:
            index = int(slide) - 1
            self.impressController.gotoSlideIndex(index)
        except:
            self.logger.error("Impossible d'executer la requête <slide n>")

    # EN CAS DE COMMANDE INCORRECT / ON IGNORE
    def unknown_command(self, command):
        self.logger.warn("Commande non trouvé : " + command)
