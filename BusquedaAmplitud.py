##################################################################################################################
########################################ALGORITMO DE BUSQUEDA POR AMPLITUD########################################
##################################################################################################################

import time
#1 Izq 2 Arr 3 Der 4 Abaj 5 Item 7 Inicio

#Funcion de sensor
#Con este sabrá a que ubicaciones se puede mover teniendo en cuenta si ya ha paso por ahi antes (mismo estado anterior)
def Sensor(lab,nodo,arbol):   
    posy = nodo.posyActual
    posx = nodo.posxActual
    izq = 0 if posx-1<0 or lab[posy][posx-1] == 1 else 1 #Si la posicion se sale del laberinto o existe un muro, no permite la acción
    arriba = 0 if posy-1<0 or lab[posy-1][posx] == 1 else 1
    der = 0 if posx+1==len(lab) or lab[posy][posx+1] == 1 else 1
    abajo = 0 if posy+1==len(lab) or lab[posy+1][posx] == 1 else 1

    arr = [izq,arriba,der,abajo]

    #Apartado para no devolverse, a menos que el estado actual sea diferente al anterior
    if (nodo.padrey != -1 and nodo.padrex != -1):
        nodoPadre = arbol[nodo.padrey][nodo.padrex]
        if nodoPadre.cantItems == nodo.cantItems and nodo.posItems == nodoPadre.posItems:
            if (nodo.operador == 1):
                arr[2] = 0
            elif (nodo.operador == 2):
                arr[3] = 0
            elif (nodo.operador == 3):
                arr[0] = 0
            else:
                arr[1] = 0

    return arr


#Funcion de movimiento, cambia la posicion actual para asignarsela al nuevo nodo
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


#Clase Nodo
#En esta se contendrán:
#Posiciones de los items tomados
#Posicion actual
#Cantidad de items tomados
#Posicion del madre en el arbol
#Operador realizado en este nodo,
#Profundidad del arbol actual
class Nodo():
    #PosItems es un arreglo ce las coordenadas de los items que ha tomado, vacio significa que no tiene ningún item
    def __init__(self,posItems,posyActual,posxActual,cantItems,padrey,padrex,operador,profundidad):
        self.posItems = posItems
        self.posyActual = posyActual
        self.posxActual = posxActual
        self.cantItems = cantItems
        self.padrey = padrey
        self.padrex = padrex
        self.operador = operador
        self.profundidad = profundidad


#Funcion que a partir del camino correcto, se devuelve en el arbol para conocer los movimientos realizados 
#Retorna un arreglo con los movimientos realizados
def PasosSolucion(arbol, posy, posx):
    dir = {1 : "Izquierda" , 2 : "Arriba" , 3 : "Derecha" , 4 : "Abajo", 7: "Inicio" }
    arr = []
    for i in range(len(arbol)-1):
        anteriory = arbol[posy][posx].padrey
        anteriorx = arbol[posy][posx].padrex
        arr.append(dir[arbol[posy][posx].operador])
        posy = anteriory
        posx = anteriorx
    return arr


#Funcion para conocer respecto a los objetos que ha tomado, si el actual que va a tomar ya se ha hecho, en ese caso no tomarlo
def LoAgarro(obj):
    aux = False
    arr = obj.posItems
    for j in arr:
        if obj.posyActual == j[0] and obj.posxActual == j[1]:
            aux = True
            break
    return aux


#Funcion principal generadora del algoritmo de amplitud y así mismo el arbol
def Arbol(estado):
    start_time = time.time()#Toma de tiempo para conocer la duración del algoritmo hasta encontrar la solución
    NodosExp = 0
    posy = -1
    posx = -1
    
    #Apartado para conocer la posición inicial dentro del laberinto
    for y in range(len(estado)):
        for x in range(len(estado[y])):
            if estado[y][x] == 2:
                posy = y
                posx = x
                break

    arbol = [[Nodo([],posy,posx,0,-1,-1, 7, 0)]] #Creacion del nodo raiz
    aux = 0 #Inicio de la profundidad
    movimientosFinales = []

    flag = False

    #Este bucle se repite hasta que se encuentre una solución, cada vez aumentará en profundidad
    while(True):
        #print("Profundidad: " + str(aux))
        #print("Largo de la fila: " + str(len(arbol[aux])))

        arbol.append([])# Aumento de profundidad inicialmente vacia
        #Bucle secundario que permite expansión y creación de los nuevos nodos
        for i in range(len(arbol[aux])):
            nodoActual = arbol[aux][i]

            #Condición respecto a si la posición actual se encuentra en un item, dependiendo de su estado será aumentado la cantidad de items o se crearán los nodos hijos
            if (estado[nodoActual.posyActual][nodoActual.posxActual] == 5):
                NodosExp += 1
                if  not(LoAgarro(nodoActual)): #Pregunta si en la posicion actual, el item que se encuentra ya ha sido tomado previamente
                    nodoActual.cantItems += 1
                    arr = []
                    arr = nodoActual.posItems.copy()
                    arr.append([nodoActual.posyActual,nodoActual.posxActual])
                    nodoActual.posItems = arr
                
                #Si la cantidad de items es igual a 2, entonces se termina el algoritmo y ya se ha encontrado una solucion
                if nodoActual.cantItems == 2:
                    flag = True
                    arr = PasosSolucion(arbol,aux,i)
                    movimientosFinales = arr[::-1]
                    #print("Profundidad: " + str(aux))
                    #print("Nodos Expandidos: " + str(NodosExp))
                    #print("Los pasos fueron: " + str(arr[::-1]))
                    #print("Tiempo total de ejecución:" + str(time.time()-start_time) + " Segundos")
                    break
                
                #Sino se tienen 2 items, entonces se crean los proximos nodos a partir del actual
                else:
                    posibilidades = Sensor(estado,nodoActual,arbol)
                    #print("1",posibilidades)
                    for j in range(len(posibilidades)):
                        if posibilidades[j] == 1:
                            posyAct,posxAct = Mover(j+1,nodoActual.posyActual,nodoActual.posxActual)
                            arbol[aux+1].append(Nodo(nodoActual.posItems,posyAct,posxAct,nodoActual.cantItems,aux,i,j+1,nodoActual.profundidad+1))
            
            #Si en la posicion actual no se encuentra un item, entonces se crean los proximos nodos a partir del actual
            else:
                NodosExp += 1
                posibilidades = Sensor(estado,nodoActual,arbol)
                for j in range(len(posibilidades)):
                    if posibilidades[j] == 1:
                        posyAct,posxAct = Mover(j+1,nodoActual.posyActual,nodoActual.posxActual)
                        arbol[aux+1].append(Nodo(nodoActual.posItems,posyAct,posxAct,nodoActual.cantItems,aux,i,j+1,nodoActual.profundidad+1))

        #Si ya se encontró una solucion, tomar el tiempo y terminar el ciclo
        if (flag):
            tiempo = str(time.time()-start_time)
            break

        #Sino aumentar la profundidad y proseguir con el algoritmo
        else:
            aux += 1

    #Seccion para observar el arbol final solamente mostrando los movimientos realizados
    """  
    for i in range(len(arbol)):
        for j in range(len(arbol[i])):
            print(arbol[i][j].operador, end =" ")
        print()
    """

    return movimientosFinales,aux,NodosExp,tiempo,posy,posx


##################################################################################################################
####################################FIN DE ALGORITMO DE BUSQUEDA POR AMPLITUD#####################################
##################################################################################################################

#ALGORITMOS DE PRUEBA
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
    [5,5]
]

maze2 = [[5,0,2,5],
[1,1,1,1],
[1,1,1,1],
[1,1,1,1],
]


