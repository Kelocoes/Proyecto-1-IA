import time
import copy

"""
Atributos de la clase
h --> Heuristica
posyActual --> posicion actual en y del agente en el lab
posxActual --> posicion actual en x del agente en el lab
posItems --> Arreglo de posiciones de los items que ha tomado
gas --> Combustible disponible
posPadre --> Posicion del padre en el arreglo de movimientosTotales
idnave --> 0 Si no tiene nave 3 Si es la nave es la de 10 4 Si es la nave de 20
"""
class Nodo():
    def __init__(self,h, posyActual, posxActual, posItems, gas, posPadre, idnave, operador):
        self.h = h
        self.posyActual = posyActual
        self.posxActual = posxActual
        self.posItems = posItems
        self.gas = gas
        self.posPadre = posPadre
        self.idnave = idnave
        self.operador = operador

#Funcion que retorna el valor de la heuristica de un nodo, utilizado para realizar el sort
def Heuristica(nodo):
    return nodo.h


#Funcion heurística, dependiendo de los items actuales y la posicion del agente, realizar la distancia de manhattan entre dos o más posiciones.
def functionH(posy,posx,posItemsReal, posItemsActual):
    if len(posItemsActual) == 0:
        shipToObject = abs(posItemsReal[0][0] - posy) + abs(posItemsReal[0][1] - posx)
        shipToObject2 = abs(posItemsReal[1][0] - posy) + abs(posItemsReal[1][1] - posx)
        objectToObject  = abs(posItemsReal[0][0] - posItemsReal[1][0]) + abs(posItemsReal[0][1] - posItemsReal[1][1])
        total  = min(shipToObject,shipToObject2) + objectToObject
        return total
    elif posItemsReal[0] != posItemsActual[0]:#Condicion para omitir items que ya han sido tomados
        return abs(posItemsReal[0][0] - posy) + abs(posItemsReal[0][1] - posx)
    else:
        return abs(posItemsReal[1][0] - posy) + abs(posItemsReal[1][1] - posx)

#Reconstruir el camino por medio del nodo solución y la lista de movimientos totales
#En la lista de movTotal busca cada uno de sus parientes y construye el camino
def ReconstruirCamino(arbol,movTotal):
    road = list()
    road.append(arbol[0])

    while road[0].posPadre != -1:
            road.insert(0,movTotal[road[0].posPadre])
    
    return road

#Funcion profundidad donde se cuenta el tamaño del nodo más profundo hasta la raíz
def getProfundidad(arbol,movTotal):
    profundidades = []
    for i in arbol:
        road = list()
        road.append(i)

        while road[0].posPadre != -1:
                road.insert(0,movTotal[road[0].posPadre])
        
        profundidades.append(len(road))
  
    return max(profundidades)

#A partir del camino encontrado, se realiza una transformación de una lista de numeros a una lista de strings donde menciona los movimientos realizados, para su posterior uso en el archivo mainProyecto1.py
def CambioMov(road):
    dir = {1 : "Izquierda" , 2 : "Arriba" , 3 : "Derecha" , 4 : "Abajo", 7: "Inicio" }
    arr = []
    for i in range(len(road)):
            arr.append(dir[road[i].operador])
            
    return arr

#Funcion sensor donde retorna los posibles movimientos que puede realizar el agente, dependiendo de:
#- Los muros
#- El estado actual y anterior del agente
def Sensor(lab,nodo,movTotal):   
    posy = nodo.posyActual
    posx = nodo.posxActual
    izq = 0 if posx-1<0 or lab[posy][posx-1] == 1 else 1 #Si la posicion se sale del laberinto o existe un muro, no permite la acción
    arriba = 0 if posy-1<0 or lab[posy-1][posx] == 1 else 1
    der = 0 if posx+1==len(lab) or lab[posy][posx+1] == 1 else 1
    abajo = 0 if posy+1==len(lab) or lab[posy+1][posx] == 1 else 1

    arr = [izq,arriba,der,abajo]
  
    #Cambio, no permitir que se devuelva, esto dependerá si el estado siguiente es exactamente igual al estado anterior del nodo actual
    if (nodo.posPadre != -1):
        padre = movTotal[nodo.posPadre]
        if (nodo.operador == 1):
            if nodo.posItems == padre.posItems and nodo.posyActual == padre.posyActual and nodo.posxActual +1 == padre.posxActual and nodo.idnave == padre.idnave:
                arr[2] = 0
        elif (nodo.operador == 2):
            if nodo.posItems == padre.posItems and nodo.posyActual + 1 == padre.posyActual and nodo.posxActual == padre.posxActual and nodo.idnave == padre.idnave:
                arr[3] = 0
        elif (nodo.operador == 3):
              if nodo.posItems == padre.posItems and nodo.posyActual == padre.posyActual and nodo.posxActual - 1 == padre.posxActual and nodo.idnave == padre.idnave :
                arr[0] = 0
        else:
            if nodo.posItems == padre.posItems and nodo.posyActual - 1 == padre.posyActual and nodo.posxActual  == padre.posxActual and nodo.idnave == padre.idnave:
                arr[1] = 0

    return arr


#Funcion de movimientos, retorna las nuevas coordenadas dependiendo de la dirección escogida
def Mover(dir,posy,posx):
    if dir == 1:
        posyActual = posy
        posxActual = posx-1
    elif dir == 2:
        posyActual = posy-1
        posxActual = posx
    elif dir == 3:
        posyActual = posy
        posxActual = posx+1
    elif dir == 4:
        posyActual = posy+1
        posxActual = posx

    return posyActual, posxActual

#Funcion que retorna si el item a escoger, ya fue agarrado previamente
def LoAgarro(posy,posx,posItems):
    aux = False
    for j in posItems:
        if posy == j[0] and posx == j[1]:
            aux = True
            break
    return aux

#Funcion que menciona si se encontró una solucion dependiendo del tamaño de posItems
def Finaliza(nodo):
    if len(nodo.posItems) == 2:
        return True
    else:
        return False


#Funcion principal
def Avara(lab):
    start_time = time.time()#Toma del tiempo actual 
    nodosExp = 0#Inicio de cantidad de nodos expandidps
    posItems = []#Arreglo donde se ubicarán la posicion de los items en el laberinto
    profundidad = 0#Tamaño de la profundidad
    movTotal = []#Arreglo donde se almacenarán los movimientos totaleso  nodos expandidos 
    posy = -1#Instancia de la posicion inicial
    posx = -1 

    #Apartado para encontrar la posicion inicial y los items
    for y in range(len(lab)):
        for x in range(len(lab[y])):
            if lab[y][x] == 2:
                posy = y
                posx = x
            elif lab[y][x] == 5:
                posItems.append([y,x])

    #Se agrega el nodo raiz en el arbol o la cola de prioridad
    arbol = [Nodo(functionH(posy,posx,posItems,[]),posy,posx, [], 0, -1, 0,7)]
    flag = False
    aux = 0
  
    while(True):
        #print("Ciclo: " + str(aux))
        arbol.sort(key = Heuristica)
        if Finaliza(arbol[0]):
            road = ReconstruirCamino(arbol,movTotal)
            nodosExp = len(movTotal) + 1
            profundidad = getProfundidad(arbol,movTotal) - 1
            movimientosFinales = CambioMov(road)
            #print(nodosExp,profundidad,movimientosFinales)
            flag = True
            break
        else:#Si el nodo actual no es el nodo final de la solucion, entonces expande a partir del primero en el arreglo
            posibilidades = Sensor(lab,arbol[0],movTotal)
            #print("1",posibilidades)
            #Por cada una de las posibilidades de movimientos, crear un nodo
            for j in range(len(posibilidades)):
                if posibilidades[j] == 1:
                    posyAct,posxAct = Mover(j+1,arbol[0].posyActual,arbol[0].posxActual)
                    posItemsNew = copy.deepcopy(arbol[0].posItems)
                    if lab[posyAct][posxAct] == 5 and not(LoAgarro(posyAct,posxAct,posItemsNew)): #Si el nodo actual se encuentre en un item y no se ha agarrado, tomarlo
                        posItemsNew.append([posyAct,posxAct])
                    arbol.append(Nodo(functionH(posyAct, posxAct, posItems, posItemsNew), posyAct, posxAct, posItemsNew, arbol[0].gas, len(movTotal), arbol[0].idnave, j+1))
            movTotal.append(arbol[0])#Mover el nodo expandido a movTotañ
            del arbol[0]#Borrar el nodo de la cola de prioridad

        aux += 1
        if (flag):
            break

    #Mostrar la cola de prioridad y el arreglo movTotal
    """
    for j in arbol:
        print(j.posyActual,j.posxActual, j.h, j.posPadre)
    print("Separador")
    for x in movTotal:
        print(x.posyActual,x.posxActual, x.h, x.posPadre)
    """
    tiempo = time.time() - start_time

    return movimientosFinales, profundidad, nodosExp, tiempo, posy, posx 


maze = [
    [0, 0, 0, 0, 0, 5, 1, 1, 4, 0], 
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
    [0, 0, 2, 6, 6, 0, 0, 0, 0, 0], 
    [1, 6, 1, 1, 1, 1, 0, 1, 1, 6], 
    [1, 6, 1, 1, 1, 1, 0, 1, 1, 6], 
    [1, 6, 1, 0, 0, 0, 0, 0, 0, 3],
    [1, 6, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 1, 1], 
    [1, 0, 0, 0, 6, 6, 6, 0, 0, 5]]


#print(maze)
#print(Avara(maze))