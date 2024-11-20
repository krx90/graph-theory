# Autor: tm, kb
# Datum: 15.07.10

from tkinter import *
from KartenGUI import *
from graph import *

g = GraphMitDatenUndRundreisen()

f_xml = open("graph_eu_6.xml", "r", encoding="latin1")
xml_quelltext = f_xml.read()
g.graphmlToGraph(xml_quelltext)
g.ersteRundreise('Bonn')

root = Tk ( )
app=KartenGUI(root, g, "Europa", 702, 600)

root.mainloop()
