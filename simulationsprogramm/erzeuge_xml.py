def erzeugeNode(knoten_quelltext):
    # beachte: knoten_sortiert.xml darf am Schluss keinen Zeilenumbruch haben.
    liste_node = []
    node_quelltext = ''
    for tupel in knoten_quelltext.split('\n'):
        if tupel != []:
            tupel_liste = tupel.split(',')
            name = tupel_liste[0]
            lat_wert = float(tupel_liste[1])
            lat_wert = lat_wert + float(tupel_liste[2])/60
            lat_wert = lat_wert + float(tupel_liste[3])/3600
            lon_wert = float(tupel_liste[4])
            lon_wert = lon_wert + float(tupel_liste[5])/60
            lon_wert = lon_wert + float(tupel_liste[6])/3600    
            liste_node = liste_node + [name]
            tag = '<node id="' + name + '">' + \
                      '<data key="lat">'+str(lat_wert)+'</data>' + \
                      '<data key="lon">'+str(lon_wert)+'</data>' + \
                      '</node>\n'
            node_quelltext = node_quelltext + tag
    return node_quelltext        
    
from math import *
def entfernung(A, B):
    x1 = A[0]/180*pi
    y1 = A[1]/180*pi
    x2 = B[0]/180*pi
    y2 = B[1]/180*pi
    return acos(sin(x2)*sin(x1) + cos(x2)*cos(x1)*cos(y2-y1))*6378.388

    
def erzeugeEdge(knoten_quelltext):
    # beachte: knoten_sortiert_ansi.txt darf am Schluss keinen Zeilenumbruch haben.
    liste_node = []
    for tupel in knoten_quelltext.split('\n'):
        if tupel != []:
            tupel_liste = tupel.split(',')
            name = tupel_liste[0]
            lat_wert = float(tupel_liste[1])
            lat_wert = lat_wert + float(tupel_liste[2])/60
            lat_wert = lat_wert + float(tupel_liste[3])/3600
            lon_wert = float(tupel_liste[4])
            lon_wert = lon_wert + float(tupel_liste[5])/60
            lon_wert = lon_wert + float(tupel_liste[6])/3600    
            liste_node = liste_node + [(name, lat_wert, lon_wert)]
    edge_quelltext = ''
    for node1 in liste_node:
        for node2 in liste_node:
            if node1 != node2:
                A = (node1[1], node1[2])
                B = (node2[1], node2[2])
                entf = '{0:.1f}'.format(entfernung(A, B))
                tag = '<edge source="' + node1[0] + \
                  '" target="' + node2[0] +'">' + \
                  '<data key="gewicht">'+str(entf)+'</data>' + \
                  '</edge>\n'
                edge_quelltext = edge_quelltext + tag
    return edge_quelltext

def erzeugeGraph():
    knoten_datei = open('knotendaten.txt', 'r')
    knoten_quelltext = knoten_datei.read()
    knoten_datei.close()
    xml_quelltext = '<?xml version="1.0" encoding="iso-8859-1"?>\n' + \
                    '<graph id="test">\n' + \
                    '<!--Knoten-->\n' + \
                    erzeugeNode(knoten_quelltext) + \
                    '<!--Kanten-->\n' + \
                    erzeugeEdge(knoten_quelltext) + \
                    '</graph>'
    node_datei = open('graph_eu.xml', 'w')
    node_datei.write(xml_quelltext)
    node_datei.close()


# Ausführung


erzeugeGraph()


