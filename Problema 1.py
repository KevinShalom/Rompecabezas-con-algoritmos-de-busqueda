from collections import deque
import random
from tabulate import tabulate  # Para mejorar la visualización del tablero

# Función para contar las inversiones
def contar_inversiones(tablero):
    inversions = 0
    for i in range(len(tablero)):
        for j in range(i + 1, len(tablero)):
            if tablero[i] != 0 and tablero[j] != 0 and tablero[i] > tablero[j]:
                inversions += 1
    return inversions

# Función para verificar si un estado es resoluble
def es_resoluble(tablero):
    return contar_inversiones(tablero) % 2 == 0

# Función para generar un estado inicial aleatorio y resoluble
def generar_estado_inicial_resoluble():
    while True:
        tablero = random.sample(range(9), 9)
        if es_resoluble(tablero):
            return tablero

# Clase Puzzle para representar el problema del 8-puzzle
class Puzzle:
    def __init__(self, tablero):
        self.tablero = tablero
        self.blank_index = tablero.index(0)  # Índice de la casilla vacía
        self.parent = None  # Para rastrear el nodo padre
    
    def __eq__(self, otro):
        return self.tablero == otro.tablero
    
    def __hash__(self):
        return hash(tuple(self.tablero))

# Función para verificar si el movimiento es válido
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

# Función para aplicar un movimiento y generar un nuevo estado
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

# Función para generar los sucesores (posibles movimientos)
def generar_sucesores(puzzle):
    movimientos = ['ARRIBA', 'ABAJO', 'IZQUIERDA', 'DERECHA']
    sucesores = []
    for movimiento in movimientos:
        if movimiento_valido(puzzle, movimiento):
            sucesores.append(aplicar_movimiento(puzzle, movimiento))
    return sucesores

# Búsqueda en Amplitud (BFS)
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
    
    return None  # Si no se encuentra solución

# Búsqueda en Profundidad (DFS)
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
    
    return None  # Si no se encuentra solución

# Función para construir el camino desde el estado inicial al objetivo
def construir_camino(puzzle):
    camino = []
    while puzzle:
        camino.insert(0, puzzle.tablero)
        puzzle = puzzle.parent
    return camino

# Función para mostrar el tablero en forma de cubo (3x3) usando tabulate
def mostrar_tablero(tablero):
    cubo = [tablero[i:i+3] for i in range(0, len(tablero), 3)]  # Dividir la lista en filas de 3
    print(tabulate(cubo, tablefmt="fancy_grid"))  # Usar tabulate para mostrar el cubo con formato

# Función principal para seleccionar el algoritmo de búsqueda
def main():
    # Generar un estado inicial resoluble
    tablero_inicial = generar_estado_inicial_resoluble()
    puzzle_inicial = Puzzle(tablero_inicial)
    
    # Estado objetivo
    tablero_objetivo = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    puzzle_objetivo = Puzzle(tablero_objetivo)
    
    # Seleccionar el algoritmo
    print("Selecciona el algoritmo de búsqueda que deseas usar:")
    print("1. Búsqueda en Amplitud (BFS)")
    print("2. Búsqueda en Profundidad (DFS)")
    opcion = input("Ingresa el número de tu opción (1 o 2): ")
    
    if opcion == '1':
        print("Usando Búsqueda en Amplitud (BFS)...")
        solucion = bfs(puzzle_inicial, puzzle_objetivo)
    elif opcion == '2':
        print("Usando Búsqueda en Profundidad (DFS)...")
        solucion = dfs(puzzle_inicial, puzzle_objetivo)
    else:
        print("Opción inválida.")
        return
    
    # Mostrar solución
    if solucion:
        print("Solución encontrada:")
        for paso, tablero in enumerate(solucion):
            print(f"Paso {paso + 1}:")
            mostrar_tablero(tablero)  # Mostrar el tablero en forma de cubo
    else:
        print("No se encontró una solución.")

# Ejecutar el programa principal
if __name__ == "__main__":
    main()
