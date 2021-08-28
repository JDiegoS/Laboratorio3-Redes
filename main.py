#Laboratorio 3 Redes

from getpass import getpass
from client import ClientDVR

import slixmpp
import json

class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)

        self.add_event_handler("session_start", self.start)
        self.add_event_handler('register', self.register)

    def start(self, event):
        self.send_presence()
        self.get_roster()

    def register(self, event):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['username'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            resp.send()
            print("Registrado correctamente")
            self.disconnect()
        except:
            print("Error al registrarse")
            self.disconnect()

termino = False
print("\nBienvenido")
while termino != True:
    opc1 = int(input("\nIngrese una opcion:\n1. Iniciar sesion \n2. Registrar nuevo usuario \n3. Salir\n"))
    if opc1 == 1:
        #Iniciar sesion
        userName = input("Ingrese el usuario: ")
        password = getpass("Ingrese la contrasena: ")

        names = open('names-e.txt')
        namesj = json.load(names)

        topo = open('topo-e.txt')
        topoj = json.load(topo)

        names.close()
        topo.close()

        id = ''
        for i in namesj['config']:
            if namesj['config'][i] == userName:
                id = i

        neighbors = topoj['config'][id]
        neighborNames = {}
        for neighbor in namesj['config']:
            if neighbor in neighbors:
                neighborNames[neighbor] = namesj['config'][neighbor]
            
        algoritmo = input("Ingrese el algoritmo que desea utilizar:\n 1. Flooding\n2. DVR\n")
        
        if algoritmo == 1:
            #Flooding
            pass
        elif algoritmo == 2:
            #DVR
            currentC = ClientDVR(userName, password, id, neighborNames)
            currentC.connect()
            currentC.process(forever=False)

    elif opc1 == 2:
        #Registrar
        newUser = input("Ingrese el usuario: ")
        newPass = getpass("Ingrese la contrasena: ")

        registerU = Register(newUser, newPass)
        registerU.register_plugin('xep_0004') ### Data Forms
        registerU.register_plugin('xep_0030') ### Service Discovery
        registerU.register_plugin('xep_0066') ### Band Data
        registerU.register_plugin('xep_0077') ### Band Registration
        registerU.connect()
        registerU.process(forever=False)

    elif opc1 == 3:
        print("Gracias por utilizar el programa")
        termino = True
    else:
        print("Esa no es una opcion")