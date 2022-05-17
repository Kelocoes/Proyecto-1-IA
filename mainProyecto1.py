import turtle as tur
import BusquedaAmplitud as BA
import AlgoritmoCostoUniformeED as Giron
import AEstrellaED as Giron2
import AlgoritmoAvara as Avara
import AlgoritmoProfundidad as Julian


##Configuración básica de la ventana por medio de turtle
def confBasica():
    vent = tur.Screen()
    vent.bgcolor("black")#Fondo de la venana
    vent.title("Laberinto agente")#Titulo de la ventana
    vent.setup(700, 700)#Tamaño de la ventana 
    vent.colormode(255)
    tur.tracer(0,0)#No animacion


## Creacion de objetos
## Clase casilla, tendrá los atributos de cada casilla 
class Casilla(tur.Turtle): 
    def __init__(self,tipo,screen_x,screen_y,posx,posy): 
        tur.Turtle.__init__(self) 
        self.tipo = tipo #Tipo de casilla
        self.posx, self.poxy  = posx, posy # Posicion de casilla en el laberinto
        self.screen_x, self.screen_y = screen_x, screen_y #Posicion de casilla en la pantalla
        self.colores = {
            0: (255,255,255),  1: (152,72,6), 2: (0,176,240), 3 : (112,173,71),
            4 : (204,192,217), 5 : (255,255,0) , 6 : (255,0,0), 7 : "#00FFAE",
            8 : "black"
            }#Posibles colores que puede tomar la casilla
        self.turtlesize(2)#Tamaño de la casilla
        self.shape("square")#Forma el turtle
        self.color(self.colores[tipo])#Color de la casilla -> Asignación
        self.penup()#Levantar el turtle
        self.goto(self.screen_x,self.screen_y)#Ir al punto seleccionado
        self.stamp()#Marcar el turtle o el cuadro


#Lectura del archivo donde se encuentra el laberinto
#Retorna el laberinto como lista de listas
def imp_amb(arch):
    file = open(arch, "r")
    maze = [[int(j) for j in i.split(" ")] for i in file]
    return maze


#Funcion adicional que permite mostra r el laberinto después de ser leido del archivo
#No retorna
def imprimirMaze(maze): 
    print(len(maze))
    for x in range(len(maze)): 
        print(len(maze))
        for y in range(len(maze[x])): 
            print(maze[x][y])


#Configuración inicial del laberinto gráficamente
#Retorna el arreglo de casillas
def conf_amb(maze):
    arreglo = [0]*len(maze)
    for y in range(len(maze)):
        aux = []
        for x in range(len(maze[y])): 
            obj = maze[y][x]
            screen_x = -288 + (x * 50) #Posicion para tener centrado el laberinto
            screen_y = 288 - (y * 50) 
            aux.append(Casilla(obj,screen_x,screen_y,x,y))
        arreglo[y] = aux
    return arreglo


## Ejecución inicial del programa
def Inicio(arregloDibujo,maze,ruta):
    print("Hola, bienvenido al solver de laberintos, ¿qué opción desea usar?" + "\n" + 
                    "Algoritmos no informados:" + "\n" +
                    "   1. Por amplitud " + "\n" +
                    "   2. Por costo uniforme " + "\n" +
                    "   3. Por profundidad" + "\n" +
                    "Algoritmos informados: " + "\n" +
                    "   4. Por Avara" + "\n" +
                    "   5. Por A* " )
    flag = True

    #Se escoge el algoritmo a usar
    while(flag):
        opcion = input()
        if int(opcion) == 1:
            flag = False
            movimientos, profundidad, nodosExpandidos, tiempo, posy, posx = BA.Arbol(maze)
            print("Posicion inicial: " + str([posy,posx]))
            print("Movimientos: " + str(movimientos))
            print("Profundidad: " + str(profundidad))
            print("Nodos expandidos: " + str(nodosExpandidos))
            print("Tiempo: " + str(tiempo) + " Segundos")
        elif int(opcion) == 2:
            flag = False
            movimientos, profundidad, nodosExpandidos, tiempo, posy, posx = Giron.busquedaCostoUniforme(ruta)
            print("Posicion inicial: " + str([posy,posx]))
            print("Movimientos: " + str(movimientos))
            print("Profundidad: " + str(profundidad))
            print("Nodos expandidos: " + str(nodosExpandidos))
            print("Tiempo: " + str(tiempo) + " Segundos")
            None
        elif int(opcion) == 3:
            flag = False
            movimientos, profundidad, nodosExpandidos, tiempo, posy, posx = Julian.algPrincipal(maze)
            print("Posicion inicial: " + str([posy,posx]))
            print("Movimientos: " + str(movimientos))
            print("Profundidad: " + str(profundidad))
            print("Nodos expandidos: " + str(nodosExpandidos))
            print("Tiempo: " + str(tiempo) + " Segundos")
            None
        elif int(opcion) == 4:
            flag = False
            movimientos, profundidad, nodosExpandidos, tiempo, posy, posx = Avara.Avara(maze)
            print("Posicion inicial: " + str([posy,posx]))
            print("Movimientos: " + str(movimientos))
            print("Profundidad: " + str(profundidad))
            print("Nodos expandidos: " + str(nodosExpandidos))
            print("Tiempo: " + str(tiempo) + " Segundos")
            None
        elif int(opcion) == 5:
            flag = False
            movimientos, profundidad, nodosExpandidos, tiempo, posy, posx = Giron2.AEstrella(ruta)
            print("Posicion inicial: " + str([posy,posx]))
            print("Movimientos: " + str(movimientos))
            print("Profundidad: " + str(profundidad))
            print("Nodos expandidos: " + str(nodosExpandidos))
            print("Tiempo: " + str(tiempo) + " Segundos")
            None
        else:
            print("Error en la elección, por favor escoja de nuevo")

    tur.tracer(1,30)#Valor por defecto del turtle velocidad
    ficha = "TurtlePersonalizado.gif"
    tur.register_shape(ficha)
    tur.shape(ficha)#Config turtle personalizado
    tur.shapesize(1.5)#Tamaño del turtle
    tur.penup()#Levantamiento del recorrido del turtle
    tur.goto(arregloDibujo[posy][posx].screen_x,arregloDibujo[posy][posx].screen_y)#Dirigir el turtle a la posicion inicial del laberinto

    #Movimientos del turtle en el laberinto
    for j in movimientos[1:]:
        if j == "Izquierda":
            tur.goto(arregloDibujo[posy][posx-1].screen_x,arregloDibujo[posy][posx-1].screen_y)
            posx -= 1
        elif j == "Arriba":
            tur.goto(arregloDibujo[posy-1][posx].screen_x,arregloDibujo[posy-1][posx].screen_y)
            posy -= 1
        elif j == "Derecha":
            tur.goto(arregloDibujo[posy][posx+1].screen_x,arregloDibujo[posy][posx+1].screen_y)
            posx += 1
        else:
            tur.goto(arregloDibujo[posy+1][posx].screen_x,arregloDibujo[posy+1][posx].screen_y)
            posy += 1
        
confBasica()
ruta = "ambiente.txt"
maze = imp_amb(ruta)
arregloDibujo = conf_amb(maze)
Inicio(arregloDibujo,maze,ruta)
tur.done()