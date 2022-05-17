#Laberinto
from inspect import currentframe
from shutil import move
import time

def AEstrella(ruta):
    #Lista vacia para el laberinto
    maze = list()
    #Almacenamiento de nodos a expandir
    movements = list() 
    #Almacenamiento de nodos expandidos
    totalmovements = list()

    """cada nodo es una lista que contiene el costo de moverse, la posicion Y y X, en ese orden,
    seguido de la bosa de items, combustible de la nave, posicion del padre en la lista,orden y heuristica
    """
    start = [0,0,0,[],0,0,0,"Inicio",0]
    #Arreglo para guardar las posiciones de los artefactos
    items = list()

    #Lectura del archivo 
    with open(ruta,"r") as file_object:
        read = file_object.read()
        readWhSpaces = read.replace(' ','')
        maze = readWhSpaces.split("\n")
        #for i in maze:
            #print(i)
    """Definiendo la funcion h(n)"""
    def funcionH(y,x,newNode):
        distanciaItem1 = abs(y - items[0][0]) + abs(x - items[0][1])
        distanciaItem2 = abs(y - items[1][0]) + abs(x - items[1][1])
        if distanciaItem1 < distanciaItem2:
            distanciaItem2 = abs(items[0][0] - items[1][0]) + abs(items[0][1] - items[1][1])
            distanciaH = distanciaItem1 + distanciaItem2
        else:
            distanciaItem1 = abs(items[1][0] - items[0][0]) + abs(items[1][1] - items[0][1])
            distanciaH = distanciaItem2 + distanciaItem1

        if len(newNode[3]) > 0:
            #print(newNode[3],items[0])
            if newNode[3][0] == items[0]:
                distanciaH = abs(y - items[1][0]) + abs(x - items[1][1])
            else:
                distanciaH = abs(y - items[0][0]) + abs(x - items[0][1])
        #if len(newNode[3]) > 1:
            #distanciaH = 0

        return distanciaH



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
        #si la posicion a la que se va a mover no es 1, puede entrar a evaluar las otras opciones
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
                newNode[3] = list(currentPos[3]) #copia la bolsa de items de su padre
                #si el estado de la bolsa es distinto al item que piensa agarrar, significa que puede recogerlo
                if currentPos[3] != [[y+1,x]]: 
                    newNode[3].append([y+1,x])
                
            if maze[y+1][x] == "6":#si el combustible de la nave es mayor a cero, moverse por aceite cuesta 1, sino 4
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[1] = newNode[1] + 1


            newNode[8] = newNode[0] + funcionH(y+1,x,newNode)
            #La posicion del padre es el ultimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            #posicion del abuelo del nodo hipotetico (NewNode)
            #Es decir granpaPos es el padre de currentPos y el abuelo de Newnode
            granpaPos = currentPos[5]

            if newNode[4] > 0:
                newNode[4] = newNode[4] -1 #Si hay combustible restele 1 uso 
            if newNode[4] == 0:
                newNode[6] = 0 #cuando no hay combustible, cambia el identificador de la nave a 0

            #Verifica si el estado del newNode es distinto al de su abuelo
            #usando como criterios Y,X,bolsa de items,identificador de la nave
            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            

        #mirar hacia la izquierda
        #si la posicion a la que se va a mover no es 1, puede entrar a evaluar las otras opciones
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
                newNode[3] = list(currentPos[3]) #copia la bolsa de items de su padre
                #si el estado de la bolsa es distinto al item que piensa agarrar, significa que puede recogerlo
                if currentPos[3] != [[y,x-1]]:
                    newNode[3].append([y,x-1])
            if maze[y][x-1] == "6":#si el combustible de la nave es mayor a cero, moverse por aceite cuesta 1, sino 4
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[2] = newNode[2] - 1

            newNode[8] = newNode[0] + funcionH(y,x-1,newNode)
            #La posicion del padre es e utimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            #posicion del abuelo del nodo hipotetico (NewNode)
            #Es decir granpaPos es el padre de currentPos y el abuelo de Newnode
            granpaPos = currentPos[5]

            
            if newNode[4] > 0:
                newNode[4] = newNode[4] -1 #Si hay combustible restele 1 uso 
            if newNode[4] == 0:
                newNode[6] = 0 #cuando no hay combustible, cambia el identificador de la nave a 0

            #Verifica si el estado del newNode es distinto al de su abuelo
            #usando como criterios Y,X,bolsa de items,identificador de la nave
            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            

        #mirar hacia arriba
        #si la posicion a la que se va a mover no es 1, puede entrar a evaluar las otras opciones
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
                newNode[3] = list(currentPos[3]) #copia la bolsa de items de su padre
                #si el estado de la bolsa es distinto al item que piensa agarrar, significa que puede recogerlo
                if currentPos[3] != [[y-1,x]]:
                    newNode[3].append([y-1,x])
            if maze[y-1][x] == "6":#si el combustible de la nave es mayor a cero, moverse por aceite cuesta 1, sino 4
                if newNode[4] > 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[1] = newNode[1] - 1
            
            newNode[8] = newNode[0] + funcionH(y-1,x,newNode)
            #La posicion del padre es e utimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            #posicion del abuelo del nodo hipotetico (NewNode)
            #Es decir granpaPos es el padre de currentPos y el abuelo de Newnode
            granpaPos = currentPos[5]

            if newNode[4] > 0:
                newNode[4] = newNode[4] -1 #Si hay combustible restele 1 uso 
            if newNode[4] == 0:
                newNode[6] = 0 #cuando no hay combustible, cambia el identificador de la nave a 0

            #Verifica si el estado del newNode es distinto al de su abuelo
            #usando como criterios Y,X,bolsa de items,identificador de la nave
            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)


        #mirar hacia la derecha
        #si la posicion a la que se va a mover no es 1, puede entrar a evaluar las otras opciones
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
                newNode[3] = list(currentPos[3]) #copia la bolsa de items de su padre
                #si el estado de la bolsa es distinto al item que piensa agarrar, significa que puede recogerlo
                if currentPos[3] != [[y,x+1]]:
                    newNode[3].append([y,x+1])
            if maze[y][x+1] == "6": #si el combustible de la nave es mayor a cero, moverse por aceite cuesta 1, sino 4
                if newNode[4]> 0:
                    newNode[0] = newNode[0] + 1
                else:
                    newNode[0] = newNode[0] + 4
                newNode[2] = newNode[2] + 1

            newNode[8] = newNode[0] + funcionH(y,x+1,newNode)
            #La posicion del padre es el ultimo indice de la lista totalmovements
            fatherPos = len(totalmovements) - 1
            newNode[5] = fatherPos

            #posicion del abuelo del nodo hipotetico (NewNode)
            #Es decir granpaPos es el padre de currentPos y el abuelo de Newnode
            granpaPos = currentPos[5]
    
            if newNode[4] > 0:
                newNode[4] = newNode[4] - 1 #Si hay combustible restele 1 uso 
            if newNode[4] == 0:
                newNode[6] = 0 #cuando no hay combustible, cambia el identificador de la nave a 0

            #Verifica si el estado del newNode es distinto al de su abuelo
            #usando como criterios Y,X,bolsa de items,identificador de la nave
            if totalmovements[granpaPos][1] != newNode[1] or totalmovements[granpaPos][2] != newNode[2] or totalmovements[granpaPos][3] != newNode[3] or totalmovements[granpaPos][6] != newNode[6]:
                movements.append(newNode)
            
        #ordenamos de menor a mayor los posibles nodos a expandir segun el coste    
        movements.sort(reverse=False, key = getFN )

    #Reconstruye el camino
    def rebuildRoad():
        road = list()
        #El ultimo item del road, sera el ultimo nodo hoja que intento expandir, el cual es la respuesta
        road.append(movements[0])  

        #Insertara en la primera posicion del road el padre del primer item en road
        #hasta que el padre del primer item del road sea 0 
        while road[0][0] != 0:
            road.insert(0,totalmovements[road[0][5]])

        return road

    def getFN(i):
        return i[8]


    #Encontrar posicion inicial y la posicion de los artefactos
    for i in range(len(maze)): 
        for j in range(len(maze[i])):
            #print(j)
            if maze[i][j] == "2":
                start[1]=i
                start[2]=j
            if maze[i][j] == "5":
                temp = list()
                temp.append(i)
                temp.append(j)
                items.append(temp)



    #Agrega como primer nodo a expandir el inicio del laberinto(Nodo raiz)
    movements.append(start)
    
    startT = time.time()
    #Mientras la bolsa de artefactos tenga menor o igual a 1, seguira buscando un camino 
    while len(movements[0][3]) <= 1:
        detecMovent(movements[0])

    end = time.time() - startT #Tiempo que tarda el algoritmo

    camino = rebuildRoad() #Camino final

    nodos = len(totalmovements) #Cantidad de nodos expandidos

    profundidades = list() #profundidad maxima del arbol

    #Realizamos el mismo procedimiento de camino usando todos los nodos hojas
    #De esta manera averiguamos cual esta mas profundo 
    #lo que nos permite ver la profundida maxima del arbol
    for i in movements:
        road = list()
        road.append(i)

        while road[0][0] != 0:
            road.insert(0,totalmovements[road[0][5]])
        
        profundidades.append(len(road))

    profundidad = max(profundidades)

    directions = list() #Direcciones que toma en "lenguaje natural" ej: "Arriba" "Abajo" "Izquierda" "Derecha"

    for i in camino:
        directions.append(i[7])
        
    #print(items,start)
    
    return directions,profundidad,nodos,end,totalmovements[0][1],totalmovements[0][2]
    #return totalmovements[0][0],"\n",camino