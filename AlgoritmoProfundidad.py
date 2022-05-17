##################################################################################################################
##########################ALGORITMO DE BUSQUEDA POR PROFUNDIADD SIN CICLOS########################################
##################################################################################################################

import time

from numpy import array
#1 Izq 2 Arr 3 Der 4 Abaj 5 Item 7 Inicio

## Implementacion clase pila
## Creamos la clase pila para el uso de este objeto en nuestro algoritmo
class Pila(): 

    def __init__(self): 
        self.items = [] ## pila vacia

    def push(self, elem): 
        self.items.append(elem) ## agrega objeto a la pila
    
    def top(self): 
        try: 
            return self.items.pop() ## retorna el objeto del tope de la pila
        except IndexError: 
            raise ValueError("Pila vacia")

    def psize(self): 
        return len(self.items) ## tamaño de la pila

    def is_empty(self): ## es vacio? 
        if (len(self.items) == 0): 
            return True
        else: 
            return False

    def getPila(self): ## devuelve la lista de la pila
        return self.items
### Implementacion clase nodo ###

#Clase Nodo
#En esta se contendrán:
#Posiciones de los items tomados
#Posicion actual
#Cantidad de items tomados
#Nodo padre -> objeto nodo que es padre del nodo actual 
#Operador realizado en este nodo,
#Profundidad del arbol actual
class Nodo():
    #PosItems es un arreglo ce las coordenadas de los items que ha tomado, vacio significa que no tiene ningún item
    def __init__(self,posItems,posyActual,posxActual,cantItems, nodoPadre, operador,profundidad):
        self.posItems = posItems
        self.posyActual = posyActual
        self.posxActual = posxActual
        self.cantItems = cantItems
        self.nodoPadre = nodoPadre
        self.operador = operador
        self.profundidad = profundidad


######################################################################################################################

## Algoritmo principal
pila = Pila()

def algPrincipal(maze): 
    start_time = time.time() ## se toma el tiempo
    posy = -1
    posx = -1

    ## Conocer la posicion inicial del objeto / bot
    for i in range(len(maze)): 
        for j in range(len(maze[i])): 
            if (maze[i][j] == 2): ## punto inicial
                posy = i 
                posx = j
                break
    aux = 0
    NodosExp = 0
    ## creacion de nodo raiz
    ##print(posx, posy)
    pila.push(Nodo([], posy, posx, 0, None, 7, 0))  ## 7 de inicio 

    flag = False
    #Este bucle se repite hasta que se encuentre una solución, cada vez aumentará en profundidad
    while(True):
        if (pila.is_empty()): 
            print("Fallo")
            break
        else: 
            nodo = pila.top()
            if (aux < nodo.profundidad): ## Se toma la profundidad mayor entre todos los nodos expandidos
                aux = nodo.profundidad

            ##print([nodo.posxActual, nodo.posyActual, nodo.cantItems])
            if (maze[nodo.posyActual][nodo.posxActual] == 5): 
                if not(LoAgarro(nodo)): 
                    nodo.cantItems += 1
                    arr = []
                    arr = nodo.posItems.copy()
                    arr.append([nodo.posyActual, nodo.posxActual])
                    nodo.posItems = arr
            
            if (nodo.cantItems == 2): 
                
                if (aux < nodo.profundidad): 
                    aux = nodo.profundidad

                NodosExp = NodosExp + 1 
                flag = True
                arr = PasosSolucion(nodo) 
                movimientosFinales = arr[::-1]
                break
            else: 
                NodosExp = NodosExp + 1 
                expandir(maze, nodo) ## se expande el nodo
    if (flag): ## termina el ciclo, se imprime el tiempo
        tiempo = str(time.time()-start_time)
        ##print(tiempo)
    ##print("Profundidad" + str(aux))
    ##print("Nodos expandidos" + str(NodosExp))
    ##print(movimientosFinales)
    return movimientosFinales,aux,NodosExp,tiempo,posy,posx ## revisar por que es +1 

def PasosSolucion(nodo):
    dir = {1 : "Izquierda" , 2 : "Arriba" , 3 : "Derecha" , 4 : "Abajo", 7: "Inicio" }
    arr = [dir[nodo.operador]]
    nodoPadre = nodo.nodoPadre
    ## se realiza un camino hasta el nodo inicial (aquel que no tiene padre) para trazar el camino del bot
    while not(nodoPadre is None): 
        arr.append(dir[nodoPadre.operador])
        nodoPadre = nodoPadre.nodoPadre
    return arr
        
def expandir(maze, nodo): 
    posibilidades = Sensor(maze, nodo)
    ##print("itt" + str(posibilidades))
    for j in range(len(posibilidades)-1,-1,-1): 
        if posibilidades[j] == 1: 
            posyAct, posxAct = Mover(j+1, nodo.posyActual, nodo.posxActual)
            nodoExpand = Nodo(nodo.posItems, posyAct, posxAct, nodo.cantItems, nodo, j+1, nodo.profundidad+1)
            pila.push(nodoExpand) ## se realiza push del nodo
            
def Mover(dir, posy, posx):
    if (dir == 1): ## izq
        posyActual = posy
        posxActual = posx-1
    elif (dir == 2): ## ariba
        posyActual = posy-1
        posxActual = posx
    elif (dir == 3):  ## der 
        posyActual = posy
        posxActual = posx+1
    elif (dir == 4): ## abajo
        posyActual = posy+1
        posxActual = posx
    return posyActual, posxActual

def LoAgarro(obj): 
    aux = False
    arr = obj.posItems
    for j in arr: 
        if obj.posyActual == j[0] and obj.posxActual == j[1]: 
            aux = True
            break
    return aux

def Sensor(lab, nodo): 
    posy = nodo.posyActual
    posx = nodo.posxActual
    izq = 0 if posx-1<0 or lab[posy][posx-1] == 1 else 1 #Si la posicion se sale del laberinto o existe un muro, no permite la acción
    arriba = 0 if posy-1<0 or lab[posy-1][posx] == 1 else 1
    der = 0 if posx+1==len(lab) or lab[posy][posx+1] == 1 else 1
    abajo = 0 if posy+1==len(lab) or lab[posy+1][posx] == 1 else 1
    
    arr = [izq, arriba, der, abajo]  # orden de operadores
    #Apartado para evitar ciclos
    for i in range(len(arr)): 
        if arr[i] == 1: 
            newposy, newposx = Mover(i+1, posy, posx)
            if (Ciclos(Nodo(nodo.posItems, newposy, newposx, nodo.cantItems, nodo, i+1, nodo.profundidad+1))): 
                arr[i] = 0; 
    ##print("Itt" + str(arr))
    return arr

def Ciclos(nodo): 
    nodoPadre = nodo.nodoPadre
    flag = False
    while not(nodoPadre is None): 
        if (nodoPadre.posxActual == nodo.posxActual and nodoPadre.posyActual == nodo.posyActual and nodoPadre.cantItems == nodo.cantItems):
            flag = True
            break
        else: 
            nodoPadre = nodoPadre.nodoPadre
    return flag


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


maze1 = [
    [2,0],
    [5,5],
]

maze2 = [[5,0,2,5],
[1,1,1,1],
[1,1,1,1],
[1,1,1,1],
]
