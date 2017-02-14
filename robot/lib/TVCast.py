"""
Choregraphe Lib
TVCast.py
======================
Librairie pour se connecter au serveur Libre Office
:platform: naoqi 2.1.4
:copyright: (c) 2017 Ville de Nevers
:license: GNU GPLv3, ouvrir LICENSE pour plus d'information.
:author: Romain B. <rb@ville-nevers.fr>
"""

import socket

class ServerConnection(object):

    HOST = 'X.X.X.X' #  IP du poste distant
    PORT = 0000 #  Port du poste distant

    def __init__(self):
        self.connected = False
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
    def connect(self):
        try:
            self.clientsocket.connect((self.HOST, self.PORT))
            self.connected = True
        except:
            self.connected = False
        
            
    def send(self, pcommand):
        if self.connected == True:
            self.clientsocket.send(pcommand)


    def close(self):
        self.clientsocket.close()
        self.connected = False
        
