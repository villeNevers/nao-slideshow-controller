"""
Choregraphe Box
slide_goto.py
======================
Aller a la diapositive definie en parametre de la box.
:platform: naoqi 2.1.4
:copyright: (c) 2017 Ville de Nevers
:license: GNU GPLv3, ouvrir LICENSE pour plus d'information.
:author: Romain B. <rb@ville-nevers.fr>
"""

import sys
import os

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)

    def onLoad(self):
        self.memory = ALProxy("ALMemory")


    def onUnload(self):
        pass

    def onInput_onStart(self):

        # Add personal lib to robot python path
        libFolder = os.path.join(self.behaviorAbsolutePath(), "../lib")
        sys.path.append(libFolder)

        # Import the lib
        import TVCast
        reload(TVCast)

        # Control SlideShow
        serverConnection = TVCast.ServerConnection()
        self.logger.info(serverConnection)
        serverConnection.connect()
        serverConnection.send("slide_" + str(self.getParameter("slide")))
        serverConnection.close()

        # Remove personal lib from robot python path
        sys.path.remove(libFolder)

        self.onStopped()


    def onInput_onStop(self):
        self.onUnload()
        self.onStopped()