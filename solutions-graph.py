# Autor: kb
# Datum: 15.07.10

class Knoten(object):
    def __init__(self, nameKnoten):
        self.name = nameKnoten
        self.kantenZuNachbarn = []

    def addNachbar(self, refKante):
        self.kantenZuNachbarn = self.kantenZuNachbarn + [(refKante)]

    def delNachbar(self, refKante):
        neueListe = []
        for kante in self.kantenZuNachbarn:
            if kante != refKante:
                neueListe = neueListe + [kante]
        self.kantenZuNachbarn = neueListe

class Kante(object):
    def __init__(self, refStartKnoten, refZielKnoten):
        self.startKnoten = refStartKnoten
        self.zielKnoten = refZielKnoten

class Graph(object):
    def __init__(self):
        self.knotenListe = []

    def getRefKnoten(self, nameKnoten):
        refKnoten = None
        for knoten in self.knotenListe:
            if knoten.name == nameKnoten:
                refKnoten = knoten
        return refKnoten
   
    def addKnoten(self, nameKnoten):
        refKnoten = self.getRefKnoten(nameKnoten)
        if refKnoten == None:
            knoten = Knoten(nameKnoten)
            self.knotenListe = self.knotenListe + [knoten]

    def delKnoten(self, nameKnoten):
        neueListe = []
        for knoten in self.knotenListe:
            if knoten.name != nameKnoten:
                neueListe = neueListe + [knoten]
                neueNachbarn = []
                for kante in knoten.kantenZuNachbarn:
                    if kante.zielKnoten.name != nameKnoten:
                        neueNachbarn = neueNachbarn + [kante]
                knoten.kantenZuNachbarn = neueNachbarn
        self.knotenListe = neueListe    

    def addKante(self, nameStartKnoten, nameZielKnoten):
        if self.existiertKnoten(nameStartKnoten) and \
           self.existiertKnoten(nameZielKnoten) and \
           not self.existiertKante(nameStartKnoten, nameZielKnoten):
            refStartKnoten = self.getRefKnoten(nameStartKnoten)
            refZielKnoten = self.getRefKnoten(nameZielKnoten)
            if refStartKnoten != None and refZielKnoten != None:
                neueKante = Kante(refStartKnoten, refZielKnoten)
                refStartKnoten.addNachbar(neueKante)

    def delKante(self, nameStartKnoten, nameZielKnoten):
        for knoten in self.knotenListe:
            if knoten.name == nameStartKnoten:
                for kante in knoten.kantenZuNachbarn:
                    if kante.zielKnoten.name == nameZielKnoten:
                        knoten.delNachbar(kante)

    def getAlleKnoten(self):
        namenKnoten = []
        for knoten in self.knotenListe:
            namenKnoten = namenKnoten + [knoten.name]
        return namenKnoten

    def getAlleNachbarn(self, nameKnoten):
        refKnoten = self.getRefKnoten(nameKnoten)
        if refKnoten != None:
            listeNachbarn = []
            for kante in refKnoten.kantenZuNachbarn:
                listeNachbarn = listeNachbarn + [kante.zielKnoten.name]
            return listeNachbarn
        else:
            return []

    def existiertKnoten(self, nameKnoten):
        if self.getRefKnoten(nameKnoten) == None:
            return False
        else:
            return True

    def existiertKante(self, nameStartKnoten, nameZielKnoten):
        gefunden = False
        refStartKnoten = self.getRefKnoten(nameStartKnoten)
        refZielKnoten = self.getRefKnoten(nameZielKnoten)
        if refStartKnoten != None and refZielKnoten != None:
            for kante in refStartKnoten.kantenZuNachbarn:
                if kante.zielKnoten == refZielKnoten:
                    gefunden = True
        return gefunden
