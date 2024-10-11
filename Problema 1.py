from collections import deque
import random
from tabulate import tabulate  # para mejorar la visualizacion del tablero

# funcion para contar las inversiones
def contar_inversiones(tablero):
    inversions = 0
    for i in range(len(tablero)):
        for j in range(i + 1, len(tablero)):
            if tablero[i] != 0 and tablero[j] != 0 and tablero[i] > tablero[j]:
                inversions += 1
    return inversions

# funcion para verificar si un estado es resoluble
def es_resoluble(tablero):
    return contar_inversiones(tablero) % 2 == 0

# funcion para generar un estado inicial aleatorio y resoluble
def generar_estado_inicial_resoluble():
    while True:
        tablero = random.sample(range(9), 9)
        if es_resoluble(tablero):
            return tablero

# clase puzzle para representar el problema del 8-puzzle
class Puzzle:
    def __init__(self, tablero):
        self.tablero = tablero
        self.blank_index = tablero.index(0)  # indice de la casilla vacia
        self.parent = None  # para rastrear el nodo padre
    
    def __eq__(self, otro):
        return self.tablero == otro.tablero
    
    def __hash__(self):
        return hash(tuple(self.tablero))

# funcion para verificar si el movimiento es valido
def movimiento_valido(puzzle, movimiento):
    fila_vacia, col_vacia = puzzle.blank_index // 3, puzzle.blank_index % 3
    if movimiento == 'ARRIBA':
        return fila_vacia > 0
    elif movimiento == 'ABAJO':
        return fila_vacia < 2
    elif movimiento == 'IZQUIERDA':
        return col_vacia > 0
    elif movimiento == 'DERECHA':
        return col_vacia < 2

# funcion para aplicar un movimiento y generar un nuevo estado
def aplicar_movimiento(puzzle, movimiento):
    nuevo_tablero = puzzle.tablero.copy()
    blank_index = puzzle.blank_index
    if movimiento == 'ARRIBA':
        nuevo_tablero[blank_index], nuevo_tablero[blank_index - 3] = nuevo_tablero[blank_index - 3], nuevo_tablero[blank_index]
    elif movimiento == 'ABAJO':
        nuevo_tablero[blank_index], nuevo_tablero[blank_index + 3] = nuevo_tablero[blank_index + 3], nuevo_tablero[blank_index]
    elif movimiento == 'IZQUIERDA':
        nuevo_tablero[blank_index], nuevo_tablero[blank_index - 1] = nuevo_tablero[blank_index - 1], nuevo_tablero[blank_index]
    elif movimiento == 'DERECHA':
        nuevo_tablero[blank_index], nuevo_tablero[blank_index + 1] = nuevo_tablero[blank_index + 1], nuevo_tablero[blank_index]
    
    nuevo_puzzle = Puzzle(nuevo_tablero)
    nuevo_puzzle.parent = puzzle
    return nuevo_puzzle

# funcion para generar los sucesores (posibles movimientos)
def generar_sucesores(puzzle):
    movimientos = ['ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA']
    sucesores = []
    for movimiento in movimientos:
        if movimiento_valido(puzzle, movimiento):
            sucesores.append(aplicar_movimiento(puzzle, movimiento))
    return sucesores

# busqueda en amplitud (bfs)
def bfs(estado_inicial, estado_objetivo):
    cola = deque([estado_inicial])
    visitados = set()
    
    while cola:
        actual = cola.popleft()
        if actual == estado_objetivo:
            return construir_camino(actual)
        
        visitados.add(actual)
        sucesores = generar_sucesores(actual)
        for sucesor in sucesores:
            if sucesor not in visitados:
                cola.append(sucesor)
                visitados.add(sucesor)
    
    return None  # si no se encuentra solucion

# busqueda en profundidad (dfs)
def dfs(estado_inicial, estado_objetivo):
    pila = [estado_inicial]
    visitados = set()
    
    while pila:
        actual = pila.pop()
        if actual == estado_objetivo:
            return construir_camino(actual)
        
        visitados.add(actual)
        sucesores = generar_sucesores(actual)
        for sucesor in sucesores:
            if sucesor not in visitados:
                pila.append(sucesor)
                visitados.add(sucesor)
    
    return None  # si no se encuentra solucion

# funcion para construir el camino desde el estado inicial al objetivo
def construir_camino(puzzle):
    camino = []
    while puzzle:
        camino.insert(0, puzzle.tablero)
        puzzle = puzzle.parent
    return camino

# funcion para mostrar el tablero en forma de cubo (3x3) usando tabulate
def mostrar_tablero(tablero):
    cubo = [tablero[i:i+3] for i in range(0, len(tablero), 3)]  # dividir la lista en filas de 3
    print(tabulate(cubo, tablefmt="fancy_grid"))  # usar tabulate para mostrar el cubo con formato

# funcion principal para seleccionar el algoritmo de busqueda
def main():
    # generar un estado inicial resoluble
    tablero_inicial = generar_estado_inicial_resoluble()
    puzzle_inicial = Puzzle(tablero_inicial)
    
    # estado objetivo
    tablero_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    puzzle_objetivo = Puzzle(tablero_objetivo)
    
    # seleccionar el algoritmo
    print("selecciona el algoritmo de busqueda que deseas usar:")
    print("1. busqueda en amplitud (bfs)")
    print("2. busqueda en profundidad (dfs)")
    opcion = input("ingresa el numero de tu opcion (1 o 2): ")
    
    if opcion == '1':
        print("usando busqueda en amplitud (bfs)...")
        solucion = bfs(puzzle_inicial, puzzle_objetivo)
    elif opcion == '2':
        print("usando busqueda en profundidad (dfs)...")
        solucion = dfs(puzzle_inicial, puzzle_objetivo)
    else:
        print("opcion invalida.")
        return
    
    # mostrar solucion
    if solucion:
        print("solucion encontrada:")
        for paso, tablero in enumerate(solucion):
            print(f"paso {paso + 1}:")
            mostrar_tablero(tablero)  # mostrar el tablero en forma de cubo
    else:
        print("no se encontro una solucion.")

# ejecutar el programa principal
if __name__ == "__main__":
    main()
