knotenliste = ['A', 'B', 'C', 'D']
adjazenzmatrix = [[0, 1, 0, 0], [0, 1, 1, 1], [1, 1, 0, 0], [0, 0, 0, 0]]

def existiertKnoten(name):
    if name in knotenliste:
        return True
    else:
        return False
    
knoten1 = input("Knoten 1? >>> ")

print(existiertKnoten(knoten1))