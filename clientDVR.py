import sys
import asyncio
import logging
from getpass import getpass
from slixmpp.xmlstream.asyncio import asyncio

import slixmpp
import time
import json

#Referencias:
# https://slixmpp.readthedocs.io/en/slix-1.6.0/getting_started/echobot.html
# https://github.com/fritzy/SleekXMPP/tree/develop/examples

class ClientDVR(slixmpp.ClientXMPP):
    def __init__(self, jid, password, nid, neighborNames):
        super().__init__(jid, password)
        self.add_event_handler('session_start', self.start)
        self.add_event_handler("message", self.message)
        self.table = {}
        self.nid = nid
        self.neighborNames = neighborNames


    def BellmanFord(self, table2, sender):
        for i in table2:
            if i in self.table:
                if i != self.id and i != sender:
                    if self.table[i] > self.table[sender] + table2[i]:
                        self.table[i] = self.table[sender] + table2[i]
            else:
                self.table[i] = self.table[sender] + table2[i]
        
        return print(self.table)

    def vectorTable(self, nodes):
        self.table = {self.id: 0}
        for neighbor in nodes:
            self.table[neighbor] = 0

    def sendTable(self):
        for i in self.neighbors:
            pass

    async def sendEcho(self, to):
        msg = {}
        msg['type'] = 'sendEcho'
        msg['Nodo fuente'] = self.jid
        msg['Nodo destino'] = to
        msg['time'] = time.time()
        self.send_message(mto=to, mbody=json.dumps(msg), mtype='normal')
        self.get_roster()
        await asyncio.sleep(1)

    async def respondEcho(self, to):
        self.get_roster()
        await asyncio.sleep(3)
        msg = {}
        msg['type'] = 'responseEcho'
        msg['Nodo fuente'] = self.jid
        msg['Nodo destino'] = to
        msg['time'] = time.time()
        try:
            self.send_message(mto=to, mbody=json.dumps(msg), mtype='normal')
        except:
            print('No se pudo enviar el mensaje')
        self.get_roster()
        await asyncio.sleep(1)
        

    async def privateChat(self):
        uName = input("Ingrese el nombre del recipiente: ")
        mssg = input("Ingrese el mensaje: ")
        try:
            self.send_message(mto=uName, mbody=mssg, mtype='chat')
            self.get_roster()
            await asyncio.sleep(1)
            print("Mensaje enviado")
        except:
            print("Error al mandar mensaje")
    
    async def message(self, msg):
        if msg['type'] in ('chat'):
            print("\nMensaje recibido de %s:\n   %s\n" % (msg['from'], msg['body']))
        elif msg['type'] in ('normal'):
            
            payload = json.loads(msg['body'])

            if payload['type'] == 'responseEcho':
                distance = time.time() - payload['time']
                for i in self.neighborNames:
                    if self.neighborNames[i] == payload['fromNode']:
                        self.table[i] = distance
                        print(self.table)
                
            elif payload['type'] == 'sendEcho':
                print(payload['fromNode'])
                await self.respondEcho(payload['fromNode'])
            
    
    async def start(self, event):
        self.send_presence()
        self.get_roster()
        await asyncio.sleep(1)
        print("\nBienvenido al programa, " + self.jid)

        for i in self.neighborNames:
            await self.sendEcho(self.neighborNames[i])

        sigue = True
        while sigue == True:
            opc2 =  int(input("\nIngrese una opcion:\n1. Mostrar Usuarios \n2. Salir\n"))
            if opc2 == 1:
                #Mensaje privado
                #await self.privateChat()
                self.get_roster()
                await asyncio.sleep(1)
            elif opc2 == 2:
                print("Hasta luego!")
                self.disconnect()
                sigue = False