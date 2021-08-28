# Laboratorio 3 Redes
# Distance-vector routing


ejemploNeighbors = {
    "type": "topo",
    "config":{
        "A": ['B', 'C'],
        "B": ['A', 'C'],
        "C": ['B', 'A']
    }
}

ejemploNombres = {
    "type":"names",
    "config":{
        'A':'foo@alumchat.xyz',
        'B':'bar@alumchat.xyz',
        'C':'sol@alumchat.xyz'}
    }


class DistanceVectorRouter():
    def __init__(self, name, id):
        self.neighbors = []
        self.table = {}
        self.name = name + "@alumchat.xyz"
        self.id = id

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

ejem = {
    "A": 0,
    "B": 1,
    "C": 5,
}
ejem2 = {
    "A": 1,
    "B": 0,
    "C": 3,
    "E": 9
}
ejem3 = {
    "A": 5,
    "B": 3,
    "C": 0,
    "D": 4
}
ejem4 = {
    "E": 2,
    "C": 4,
    "D": 0
}
ejem5 = {
    "B": 9,
    "E": 0,
    "D": 2
}

dvr = DistanceVectorRouter('sol', 'A')
dvr.table = ejem
dvr.BellmanFord(ejem3, 'C')
dvr.BellmanFord(ejem2, 'B')

dvr2 = DistanceVectorRouter('sol', 'B')
dvr2.table = ejem2
dvr2.BellmanFord(ejem3, 'C')
dvr2.BellmanFord(ejem, 'A')
dvr2.BellmanFord(ejem5, 'E')


dvr3 = DistanceVectorRouter('sol', 'C')
dvr3.table = ejem3
dvr3.BellmanFord(ejem2, 'B')
dvr3.BellmanFord(ejem, 'A')
dvr3.BellmanFord(ejem4, 'D')

dvr.BellmanFord(ejem3, 'C')
dvr.BellmanFord(ejem2, 'B')