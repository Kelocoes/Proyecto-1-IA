#Laberinto
from inspect import currentframe
from shutil import move
import time

def busquedaCostoUniforme():
    maze = list()
    #Movimientos
    movements = list() 
    totalmovements = list()
    """cada nodo es una lista que contiene el costo de moverse, la posicion Y y X, en ese orden,
    seguido de la bosa de items, combustible de la nave, posicion del padre en la lista,orden
    """
    start = [0,0,0,[],0,0,0,"Inicio"]
    #Lectura del archivo 
    with open("Prueba1.txt","r") as file_object:
        read = file_object.read()
        readWhSpaces = read.replace(' ','')
        maze = readWhSpaces.split("\n")
        #for i in maze:
            #print(i)

    """Definiendo la funcion que se utiliza ver los
    movimientos posibles, recordar que el orden de las
    coordenadas es Y,X"""

    def detecMovent(currentPos):

        #Asignamos las coordenadas actuales
        y = currentPos[1]
        x = currentPos[2]
        #Copiamos la posicion actual en totalmovments y la sacamos de movements
        totalmovements.append(currentPos)
        del movements[0]
        #mirar hacia abajo
        if y+1 <= 9 and maze[y+1][x] != "1":
            newNode = list(currentPos)
            newNode[7] = "Abajo"
            if maze[y+1][x] == "0" or maze[y+1][x] == "2":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] + 1
            if maze[y+1][x] == "3":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] + 1
                if newNode[4] == 0:
                    newNode[4] = 11
                    newNode[6] = 3
            if maze[y+1][x] == "4":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] + 1
                if newNode[4] == 0:
                    newNode[4] = 21
                    newNode[6] = 4
            if maze[y+1][x] == "5":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] + 1
                newNode[3] = list(currentPos[3])
                if currentPos[3] != [[y+1,x]]:
                    newNode[3].insert(0,[y+1,x])
            if maze[y+1][x] == "6":
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[1] = newNode[1] + 1


                    
            #La posicion del padre es el ultimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            granpaPos = currentPos[5]

            if newNode[4] > 0:
                newNode[4] = newNode[4] -1
            if newNode[4] == 0:
                newNode[6] = 0

            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            

        #mirar hacia la izquierda
        if x-1 >= 0 and maze[y][x-1] != "1":
            newNode = list(currentPos)
            newNode[7] = "Izquierda"
            if maze[y][x-1] == "0" or maze[y][x-1] == "2":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] - 1
            if maze[y][x-1] == "3":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] - 1
                if newNode[4] == 0:
                    newNode[4] = 11
                    newNode[6] = 3
            if maze[y][x-1] == "4":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] - 1
                if newNode[4] == 0:
                    newNode[4] = 21
                    newNode[6] = 4
            if maze[y][x-1] == "5":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] - 1
                newNode[3] = list(currentPos[3])
                if currentPos[3] != [[y,x-1]]:
                    newNode[3].insert(0,[y,x-1])
            if maze[y][x-1] == "6":
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[2] = newNode[2] - 1


            #La posicion del padre es e utimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            granpaPos = currentPos[5]

            if newNode[4] > 0:
                newNode[4] = newNode[4] -1
            if newNode[4] == 0:
                newNode[6] = 0

            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            

        #mirar hacia arriba
        if y-1 >= 0 and maze[y-1][x] != "1":
            newNode = list(currentPos)
            newNode[7] = "Arriba"
            if maze[y-1][x] == "0" or maze[y-1][x] == "2":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] - 1
            if maze[y-1][x] == "3":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] - 1
                if newNode[4] == 0:
                    newNode[4] = 11
                    newNode[6] = 3
            if maze[y-1][x] == "4":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] - 1
                if newNode[4] == 0:
                    newNode[4] = 21
                    newNode[6] = 4
            if maze[y-1][x] == "5":
                newNode[0] = newNode[0] + 1
                newNode[1] = newNode[1] - 1
                newNode[3] = list(currentPos[3])
                if currentPos[3] != [[y-1,x]]:
                    newNode[3].insert(0,[y-1,x])
            if maze[y-1][x] == "6":
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[1] = newNode[1] - 1
            

            #La posicion del padre es e utimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            granpaPos = currentPos[5]

            if newNode[4] > 0:
                newNode[4] = newNode[4] -1
            if newNode[4] == 0:
                newNode[6] = 0

            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)


        #mirar hacia la derecha
        if x+1 <= 9 and maze[y][x+1] != "1":
            newNode = list(currentPos)
            newNode[7] = "Derecha"
            if maze[y][x+1] == "0" or maze[y][x+1] == "2":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] + 1
            if maze[y][x+1] == "3":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] + 1
                if newNode[4] == 0:
                    newNode[4] = 11
                    newNode[6] = 3
            if maze[y][x+1] == "4":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] + 1
                if newNode[4] == 0:
                    newNode[4] = 21
                    newNode[6] = 4
            if maze[y][x+1] == "5":
                newNode[0] = newNode[0] + 1
                newNode[2] = newNode[2] + 1
                newNode[3] = list(currentPos[3])
                if currentPos[3] != [[y,x+1]]:
                    newNode[3].insert(0,[y,x+1])
            if maze[y][x+1] == "6":
                if newNode[4]> 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[2] = newNode[2] + 1
        
            #La posicion del padre es el ultimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            granpaPos = currentPos[5]
    
            if newNode[4] > 0:
                newNode[4] = newNode[4] - 1
            if newNode[4] == 0:
                newNode[6] = 0

            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            
        #ordenamos de menor a mayor los posibles nodos a expandir segun el coste    
        movements.sort(reverse=False)

    #Reconstruye el camino
    def rebuildRoad():
        road = list()
        road.append(movements[0])


        while road[0][0] != 0:
            road.insert(0,totalmovements[road[0][5]])

        return road


    #Encontrar posicion inicial 
    for i in range(-1,len(maze)): 
        row = maze[i]
        for j in range(0,len(row)):
            #print(j)
            if row[j] == "2":
                start[1]=i
                start[2]=j

    movements.append(start)

    start = time.time()
    #Mientras la bolsa de artefactos tenga menos de 2, seguira buscando un camino 
    while len(movements[0][3]) <= 1:
        detecMovent(movements[0])

    end = time.time() - start

    camino = rebuildRoad()

    nodos = len(totalmovements)

    profundidades = list() 

    for i in movements:
        road = list()
        road.append(i)

        while road[0][0] != 0:
            road.insert(0,totalmovements[road[0][5]])
        
        profundidades.append(len(road))

    profundidad = max(profundidades)

    directions = list()

    for i in camino:
        directions.append(i[7])
        
    
    
    return directions,profundidad,nodos,end,totalmovements[0][1],totalmovements[0][2]

