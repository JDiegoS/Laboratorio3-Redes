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
        #Se utiliza Bellman Ford para actualizar las tablas
        for i in table2:
            if i in self.table:
                if i != self.id and i != sender:
                    if self.table[i] > self.table[sender] + table2[i]:
                        self.table[i] = self.table[sender] + table2[i]
            else:
                self.table[i] = self.table[sender] + table2[i]
        
        return print(self.table)

    async def sendEcho(self, to):
        #Enviar mensaje de echo para medir distancia
        msg = {}
        msg['type'] = 'sendEcho'
        msg['Nodo fuente'] = self.jid
        msg['Nodo destino'] = to
        msg['time'] = time.time()
        self.send_message(mto=to, mbody=json.dumps(msg), mtype='normal')
        self.get_roster()
        await asyncio.sleep(1)

    async def respondEcho(self, to):
        #Responder a un mensaje echo
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
        #Mandar un mensaje privado
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
        #Al recibir mensaje verificar que tipo de mensaje es

        if msg['type'] in ('chat'):
            print("\nMensaje recibido de %s:\n   %s\n" % (msg['from'], msg['body']))
        elif msg['type'] in ('normal'):
            payload = json.loads(msg['body'])
            if payload['type'] == 'responseEcho':
                #Recibio una respuesta de mensaje echo y puede actualizar su tabla
                distance = time.time() - payload['time']
                for i in self.neighborNames:
                    if self.neighborNames[i] == payload['fromNode']:
                        self.table[i] = distance
                        print("Tabla:\n" + self.table)
                
            elif payload['type'] == 'sendEcho':

                #Recibio una solicitud de mensaje echo entonces la responde
                await self.respondEcho(payload['fromNode'])
            
    
    async def start(self, event):
        self.send_presence()
        self.get_roster()
        await asyncio.sleep(1)
        print("\nBienvenido al programa, " + self.jid)

        sigue = True
        while sigue == True:
            opc2 =  int(input("\nIngrese una opcion:\n1. Enviar mensaje (echo) \n2. Salir\n0. Notificaciones\n"))
            if opc2 == 0:
                #Notificaciones / refresh
                self.get_roster()
                await asyncio.sleep(1)
            elif opc2 == 1:
                #Mandar echo
                for i in self.neighborNames:
                    await self.sendEcho(self.neighborNames[i])
            elif opc2 == 2:
                #Mensasje privado
                await self.privateChat()
            elif opc2 == 3:
                #Salir del programa
                print("Hasta luego!")
                self.disconnect()
                sigue = False