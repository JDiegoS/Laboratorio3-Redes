import logging
from getpass import getpass
from argparse import ArgumentParser
from flooding import *

import slixmpp
from slixmpp import ClientXMPP
from slixmpp.exceptions import IqError, IqTimeout
import uuid
import json


class ClientFlooding(slixmpp.ClientXMPP):
    def __init__(self, jid, password, recipient, message):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.recipient = recipient
        self.msg = message
        self.jid = jid
        self.previousid = []

        self.add_event_handler('session_start', self.start)
        self.add_event_handler("message", self.message)
        self.add_event_handler("register", self.register)
        print(self.recipient)
        print(self.jid)
        print(self.msg)

    async def start(self, event):
        print("Flooding start")
        self.send_presence()
        await self.get_roster()

        data = {
            "Nodo fuente": self.jid,
            "Nodo destino": self.recipient,
            "Saltos": 0,
            "Distancia": 0,
            "Listado de nodos": [],
            "Mensaje": self.message,
            "ID": str(uuid.uuid4())
        }

        self.previousid.append(data["ID"])

        print(data)

        receivers, message = flooding(json.dumps(data), self.jid)

        for receiver in receivers:
            print("Sending a Message!!!")
            self.send_message(mto=receiver,
                              mbody=message,
                              mtype='chat'
                              )

    def register(self, iq):
        iq = self.Iq()
        iq["type"] = "set"
        iq["register"]["username"] = self.boundjid.user
        iq["register"]["password"] = self.password

        try:
            iq.send()
            print("User created: " + self.boundjid + "\n")
            self.disconnect()
        except IqError:
            print("Unable to create user!\n")
            self.disconnect()
        except IqTimeout:
            print("Cannot connect with server!\n")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()

    def message(self, msg):
        if msg["type"] in ("chat"):
            recipient = str(msg["from"]).split("/")[0]
            body = msg["body"]
            data = eval(str(body))

            if(data["ID"] not in self.previousid):
                self.previousid.append(data["ID"])

                receivers, message = flooding(str(body), self.jid)

                for receiver in receivers:
                    print("Sending a Message!!!")
                    if(receiver != recipient):
                        self.send_message(mto=receiver,
                                          mbody=message,
                                          mtype='chat')
