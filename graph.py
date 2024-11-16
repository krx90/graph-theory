knotenliste = ['A', 'B', 'C', 'D']
adjazenzmatrix = [[0, 1, 0, 0], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]]

def existiertKnoten(name):
    if name in knotenliste:
        print("True")
        return True
    else:
        print("False")
        return False

existiertKnoten('A')


def existiertKante(Startknoten, Endknoten):
    if adjazenzmatrix[knotenliste.index(Startknoten)][knotenliste.index(Endknoten)] == 1:
        print("True")
        return True
    else: 
        print("False")
        return False
    
existiertKante('A', 'B')


def getAlleNachbarn(knoten):
    ergebnis = ''
    for i in range(len(adjazenzmatrix[knotenliste.index(knoten)])):
        if adjazenzmatrix[knotenliste.index(knoten)][i] > 0:
            ergebnis = ergebnis + knotenliste[i] + ' ' 
    print('Nachbarn: ' + ergebnis)        


getAlleNachbarn('B')
