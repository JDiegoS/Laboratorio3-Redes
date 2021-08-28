import json


def flooding(message, jid):
    print("flooding algorithm")
    topoJSON = open('topo-e.txt')
    topoData = json.load(topoJSON)['config']
    receivers = []
    for i in topoData[""][jid]:
        receivers.append(i)
    print("RECEIVERS: ")
    print(receivers)
    return receivers, message


# class FloodingNode():
#   def __init__(self, jid, )
