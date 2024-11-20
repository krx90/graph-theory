# Autor: tm, kb
# Datum: 15.07.10

# Importiere alles aus der tkInter-Bibliothek (Oberfläche)
from tkinter import *
# Minidom zur Interpretation der XML-Daten für die Bilddatei
from xml.dom import minidom

# Importiere gemeinsam genutzte Datentypen
from KartenTypen import *

from math import *



# Gui-Klasse (vor allem für Dijkstra-Algorithmus)
# Auf den eingegebenen Startort (bzw. Zielort) kann mit <guiobjekt>.Startort.get() zugegriffen werden.
# Die Operation, die für btnExec ausgeführt wird, muss im Hauptprogramm mit <guiobjekt>.btnExec.bind(...) definiert werden.

class KartenGUI:
    def __init__(self, master, graph, Datei, Fensterbreite, Fensterhoehe):

        self.Debug=0

        self.parentControl=master
        self.g = graph
        # Bilddaten
        self.bgBild = PhotoImage(file="%s.gif" % Datei)
        # Leinwand mit Scrollbars
        self.canBild=Canvas(master, width=Fensterbreite, height=Fensterhoehe, scrollregion=(0, 0, self.bgBild.width(), self.bgBild.height()))
        self.canBild.create_image(0,0,image=self.bgBild,anchor="nw")
        self.sbary=Scrollbar()
        self.sbary.config(command=self.canBild.yview)
        self.canBild.config(yscrollcommand=self.sbary.set)

        self.sbarx=Scrollbar()
        self.sbarx.config(command=self.canBild.xview, orient=HORIZONTAL)
        self.canBild.config(xscrollcommand=self.sbarx.set)
        # Button nächste Rundreise
        self.btnNext = Button(master,text="Nächste Rundreise")
        self.btnNext.bind('<Button-1>', self.next_ausfuehren)
        self.btnNext.grid(column=0, row=0)
        # Label für die Länge der Rundreise
        self.lblLaengeNext=Label(master, text="Länge:")
        self.lblLaengeNext.grid(column=1,row=0)        
        # Button Ende
        self.btnClose = Button(master,text="Ende")
        self.btnClose.bind("<Button-1>", self.btnCloseClick)
        self.btnClose.grid(column=5, row=0, sticky=E)

        self.canBild.grid(columnspan=6)
        self.sbary.grid(column=6,row=1, sticky=N+S)
        self.sbarx.grid(columnspan=6,sticky=E+W)

        # Fenster darf nicht in der Größe geändert werden
        master.resizable(0,0)

        # Textdatei in XML-Struktur einlesen
        try:
            baum = minidom.parse("%s.xml" % Datei)

            L=baum.getElementsByTagName("sued")[0]
            self.cSued=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("nord")[0]
            self.cNord=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("west")[0]
            self.cWest=float(L.getAttribute("wert"))
            L=baum.getElementsByTagName("ost")[0]
            self.cOst =float(L.getAttribute("wert"))
        except Exception as e:
            print("!!!FEHLER in XML-Beschreibung:", e.message)
            cNord=cSued=cWest=cOst=0.0
            raise e

        

    def btnCloseClick(self, event):
        self.parentControl.destroy()
        

    def InPixel(self, latitude, longitude):
        xProjektion = 131.579*( cos( latitude*pi/180 )*sin( (longitude-10)*pi/180 ) ) * ( ((1 + sin( latitude*pi/180 )*sin( 52*pi/180 ) + cos( latitude*pi/180 )*cos( 52*pi/180 )*cos( (longitude-10)*pi/180 ) ) *0.5)** -0.5)- (-36.388)
        yProjektion = 55.11 - 153.610*( cos( 52* pi/180)*sin( latitude*pi/180 ) - sin( 52*pi/180 )*cos( latitude*pi/180 )*cos( (longitude-10)*pi/180 ) ) * ( ((1 + sin( latitude*pi/180 )*sin( 52*pi/180 )+ cos( latitude*pi/180 )*cos( 52*pi/180 )*cos( (longitude-10)*pi/180 ) ) *0.5)** -0.5)
        x = round(xProjektion/100*self.bgBild.width())
        y = round(yProjektion/100*self.bgBild.height())
        return (x, y)


    def ZeichneOrt(self, Ort):
        if self.Debug:
            print("Call ZeichneOrt", Ort.tupel())
        Groesse=2  #Ort.Einwohner//10000
        latitude = float(self.g.getKnotenDaten(Ort, 'lat'))
        longitude = float(self.g.getKnotenDaten(Ort, 'lon'))
        (x, y) = self.InPixel(latitude, longitude)
        self.canBild.create_oval(x-Groesse,y-Groesse,x+Groesse,y+Groesse, fill = "red")
        #self.canBild.create_text(x+5,y,text=Ort.Name, fill='black', anchor="nw")


    def ZeichneWeg(self,Breite1,Laenge1,Breite2,Laenge2, Farbe="red", Dicke=1):
        if self.Debug:
            print("Call ZeichneWeg", (Breite1,Laenge1),(Breite2,Laenge2))
        (x1, y1) = self.InPixel(Breite1, Laenge1)
        (x2, y2) = self.InPixel(Breite2, Laenge2)
        self.canBild.create_line(x1,y1,x2,y2,fill=Farbe, width=Dicke)
 		
		
    def ZeichneWegListe(self,Ortsliste):
        if self.Debug:
            print("Call ZeichneWegListe", Ortsliste)
        Ort1=Ortsliste[0]
        for Ort2 in Ortsliste[1:]:
            latOrt1 = float(self.g.getKnotenDaten(Ort1, 'lat'))
            lonOrt1 = float(self.g.getKnotenDaten(Ort1, 'lon'))
            latOrt2 = float(self.g.getKnotenDaten(Ort2, 'lat'))
            lonOrt2 = float(self.g.getKnotenDaten(Ort2, 'lon'))
            self.ZeichneWeg(latOrt1,lonOrt1,latOrt2,lonOrt2)
            Ort1=Ort2


    def ausfuehren(self, event):
        self.lblLaengeOptimal.config(text='bitte warten')
        self.canBild.delete(ALL)
        self.canBild.create_image(0,0,image=self.bgBild,anchor="nw")
        (minRoute, minLaenge) = self.g.minRundreise('Bonn')
        self.lblLaengeOptimal.config(text='Länge: ' + str(minLaenge))
        
        orte = self.g.getAlleKnoten()
        for ort in orte:
            self.ZeichneOrt(ort)
        ort1 = minRoute[0]
        for ort in minRoute[1:]:
            ort2 = ort
            self.ZeichneWegListe([ort1, ort2])
            ort1 = ort2

    def next_ausfuehren(self, event):
        route = self.g.route
        laenge = self.g.laenge(route)
        self.lblLaengeNext.config(text='Länge: ' + str(laenge))
        print(route, ':', laenge)
        self.canBild.delete(ALL)
        self.canBild.create_image(0,0,image=self.bgBild,anchor="nw")
        orte = self.g.getAlleKnoten()
        for ort in orte:
            self.ZeichneOrt(ort)
        ort1 = route[0]
        for ort in route[1:]:
            ort2 = ort
            self.ZeichneWegListe([ort1, ort2])
            ort1 = ort2
        self.g.naechsteRundreise('Bonn')
