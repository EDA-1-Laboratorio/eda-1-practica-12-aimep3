"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo : Parte 3 – El ratón en el laberinto

Instrucciones generales
    Implementa las funciones en el orden en que aparecen.
    Los comentarios guiados te explican cómo razonar cada paso.
    La visualización del backtracking es OBLIGATORIA; es el corazón
    de esta parte de la práctica.

Ejecuta este archivo directamente para ver los resultados:
    python3 laberinto.py
"""

import time

# ============================================================
# LABERINTOS DE PRUEBA (ya definidos — no modificar)
# ============================================================

# 0 = celda libre, 1 = pared
LABERINTO_5x5 = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]

LABERINTO_SIN_SALIDA = [
    [0, 0, 0],
    [0, 1, 1],
    [0, 1, 0],
]

LABERINTO_SIMPLE = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]


# ============================================================
# PARTE 3A – BACKTRACKING: ENCONTRAR UN CAMINO
# ============================================================
#
# CONTEXTO DEL PROBLEMA:
# Dado un laberinto (lista de listas de 0 y 1), encuentra un camino
# de la celda (0,0) a la celda (filas-1, cols-1).
# El ratón puede moverse en las cuatro direcciones: arriba, abajo,
# izquierda y derecha.
#
# ESTRUCTURA DEL BACKTRACKING:
# El algoritmo de backtracking sigue este patrón en cada celda (fila, col):
#
# 1. VERIFICAR CONDICIONES DE PARADA (casos base):
# a) ¿Estamos fuera del laberinto? → False (movimiento inválido)
# b) ¿Es una pared? → False
# c) ¿Ya visitamos esta celda? → False (evita ciclos infinitos)
# d) ¿Llegamos a la salida? → True (¡éxito!)
#
# 2. MARCAR como visitada (la agregamos al conjunto 'visitados' y a 'ruta').
#
# 3. EXPLORAR recursivamente los cuatro vecinos:
# Si alguno retorna True, propagamos ese True hacia arriba.
#
# 4. DESMARCAR (backtrack): si ningún vecino llevó a la salida,
# quitamos la celda del conjunto 'visitados' y de 'ruta'.
# Retornamos False para indicar que por aquí no hay camino.
#
# PREGUNTA CLAVE para entender el backtrack:
# ¿Por qué hay que "desmarcar" la celda al retroceder?
# Porque otro camino que llegue a esta celda desde una dirección
# distinta sí podría tener éxito. Si la dejamos marcada permanentemente,
# la descartaríamos injustamente.
#
# NOTA SOBRE 'visitados' vs 'ruta':
# 'visitados' → set de tuplas (fila, col). Sirve para NO entrar en
# ciclos durante la exploración.
# 'ruta' → lista de tuplas (fila, col). Guarda el camino desde
# el inicio hasta la posición actual. Si encontramos la
# salida, 'ruta' contiene el camino completo.


def existe_camino(laberinto: list, fila: int, col: int,
                  visitados: set, ruta: list, contador=None, verbose=False) -> bool:
    """
    Determina si existe un camino de (fila, col) a la salida.

    Parámetros:
        laberinto – matriz de 0s y 1s.
        fila, col – posición actual del ratón.
        visitados – conjunto de celdas ya visitadas en el recorrido actual.
        ruta – lista que acumula el camino actual (se modifica in-place).
        contador – lista mutable con un entero para el número de paso (opcional).
        verbose – si True, imprime el estado del laberinto en cada paso.

    Retorna:
        True si encontró un camino (ruta contiene el camino completo).
        False si no hay camino desde esta posición.

    CÓMO PENSARLO — sigue el patrón descrito en el CONTEXTO:
    """
    filas = len(laberinto)
    cols = len(laberinto[0])

    # PASO 1a – Verifica si (fila, col) está FUERA de los límites del laberinto.
    if fila < 0 or fila >= filas or col < 0 or col >= cols:
        return False

    # PASO 1b – Verifica si la celda es una PARED.
    if laberinto[fila][col] == 1:
        return False

    # PASO 1c – Verifica si la celda ya fue VISITADA.
    if (fila, col) in visitados:
        return False

    # PASO 1d – Verifica si llegamos a la SALIDA.
    if fila == filas-1 and col == cols-1:
        ruta.append((fila, col))
        if verbose and contador is not None:
            contador[0] += 1
            imprimir_laberinto(laberinto, visitados, ruta, contador[0])
        return True

    # PASO 2 – Marca la celda como visitada.
    visitados.add((fila, col))
    ruta.append((fila, col))

    if verbose and contador is not None:
        contador[0] += 1
        imprimir_laberinto(laberinto, visitados, ruta, contador[0])

    # PASO 3 – Explora recursivamente los cuatro vecinos.
    direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)] # abajo, derecha, arriba, izquierda
    for df, dc in direcciones:
        nueva_fila = fila + df
        nueva_col = col + dc
        if existe_camino(laberinto, nueva_fila, nueva_col, visitados, ruta, contador, verbose):
            return True

    # PASO 4 – BACKTRACK: ningún vecino condujo a la salida.
    visitados.discard((fila, col))
    ruta.pop()
    if verbose and contador is not None:
        contador[0] += 1
        imprimir_laberinto(laberinto, visitados, ruta, contador[0])
    return False


# ============================================================
# PARTE 3B – VISUALIZACIÓN DEL BACKTRACKING
# ============================================================
#
# Esta función ES OBLIGATORIA. Sin ella no puedes completar el análisis
# del reporte. Llámala dentro de existe_camino para ver cada paso.

def imprimir_laberinto(laberinto: list, visitados: set,
                       ruta: list, paso: int) -> None:
    """
    Imprime el estado actual del laberinto durante el backtracking.

    Leyenda:
        S → inicio (0,0)
        E → salida (filas-1, cols-1)
        · → celda en la ruta actual (camino activo)
        * → celda visitada pero ya descartada (backtrack ocurrido)
        # → pared
        . → celda libre no visitada

    Parámetros:
        laberinto – la matriz original.
        visitados – celdas actualmente marcadas como visitadas.
        ruta – camino activo desde el inicio hasta la posición actual.
        paso – número de llamada recursiva (para identificar el paso).

    CÓMO PENSARLO:
        Recorre todas las celdas del laberinto.
        Para cada celda (i, j), decide qué símbolo imprimir:
            1. Si es (0,0) → 'S'
            2. Si es la salida → 'E'
            3. Si laberinto[i][j] == 1 → '#'
            4. Si (i,j) in ruta (usa el conjunto o la lista) → '·'
            5. Si (i,j) in visitados (pero no en ruta) → '*'
            6. De lo contrario → '.'

        Separa las celdas con espacios para mejor lectura.
        Imprime "--- Paso N ---" antes del tablero.
    """
    filas = len(laberinto)
    cols = len(laberinto[0])
    ruta_set = set(ruta) # conversión a set para búsqueda O(1)

    # PASO 1 – Imprime el encabezado del paso.
    print(f"\n--- Paso {paso} ---")

    # PASO 2 – Recorre las filas y columnas.
    for i in range(filas):
        fila_str = []
        for j in range(cols):
            if i == 0 and j == 0:
                fila_str.append('S')
            elif i == filas-1 and j == cols-1:
                fila_str.append('E')
            elif laberinto[i][j] == 1:
                fila_str.append('#')
            elif (i, j) in ruta_set:
                fila_str.append('·')
            elif (i, j) in visitados:
                fila_str.append('*')
            else:
                fila_str.append('.')
        print(' '.join(fila_str))


def encontrar_camino(laberinto: list, verbose: bool = False) -> list | None:
    """
    Wrapper que inicializa estructuras y llama a existe_camino.

    Parámetros:
        laberinto – la matriz del laberinto.
        verbose – si True, activa la visualización paso a paso.

    Retorna:
        Lista de tuplas (fila, col) con el camino encontrado, o None.

    CÓMO PENSARLO:
        Esta función no tiene lógica compleja; solo inicializa las
        estructuras necesarias y llama a existe_camino desde (0,0).

        Si verbose=True, debes pasar el contador de pasos a la función
        recursiva. Una forma limpia es usar una lista de un elemento
        como "contador mutable" que la función anidada puede modificar:
            pasos = [0]
        y dentro de existe_camino (si decides anidarla aquí):
            pasos[0] += 1
            imprimir_laberinto(laberinto, visitados, ruta, pasos[0])

        Para simplificar, puedes ignorar verbose por ahora e imprimir
        siempre, o añadir la lógica condicional más tarde.
    """
    visitados = set()
    ruta = []
    contador = [0] if verbose else None
    # Llama a existe_camino desde la posición inicial (0, 0).
    if existe_camino(laberinto, 0, 0, visitados, ruta, contador, verbose):
        return ruta
    else:
        return None


# ============================================================
# PARTE 3C – CONTAR TODOS LOS CAMINOS
# ============================================================
#
# DIFERENCIA CLAVE con encontrar_camino:
# - encontrar_camino: se DETIENE al hallar el primer camino.
# - contar_caminos: CONTINÚA explorando TODOS los caminos.
#
# Para continuar explorando, cuando llegamos a la salida NO retornamos
# inmediatamente. En cambio, sumamos 1 y seguimos explorando el resto.
# Esto requiere SIEMPRE hacer backtrack (incluso en la salida) para
# permitir que el camino se "deshaga" y se explore otra variación.
#
# ESTRUCTURA:
# contar_caminos(laberinto, fila, col, visitados):
# → si fuera de límites / pared / visitada: return 0
# → marca como visitada
# → si es la salida: cantidad = 1 (encontramos UN camino)
# de lo contrario: cantidad = suma de los cuatro vecinos recursivos
# → SIEMPRE desmarca (backtrack)
# → return cantidad


def contar_caminos(laberinto: list, fila: int, col: int,
                   visitados: set) -> int:
    """
    Cuenta todos los caminos distintos de (fila, col) a la salida.

    Retorna:
        Número de caminos válidos.

    CÓMO PENSARLO:
        La estructura es casi idéntica a existe_camino, con dos cambios:

        CAMBIO 1: En lugar de retornar True al llegar a la salida,
                  iniciamos la cuenta en 1 (este camino cuenta).
                  Luego TAMBIÉN hacemos backtrack para poder contar
                  otros caminos que pasen por la misma celda de salida
                  desde otras rutas.

        CAMBIO 2: En el caso recursivo, en lugar de retornar True
                  si ALGÚN vecino lo hace, SUMAMOS todos los resultados:
                      cantidad = 0
                      for df, dc in direcciones:
                          cantidad += contar_caminos(..., fila+df, col+dc, visitados)

        Al final, siempre hacemos backtrack (visitados.discard)
        y retornamos cantidad.
    """
    filas = len(laberinto)
    cols = len(laberinto[0])

    # PASO 1a – Fuera de límites
    if fila < 0 or fila >= filas or col < 0 or col >= cols:
        return 0

    # PASO 1b – Pared
    if laberinto[fila][col] == 1:
        return 0

    # PASO 1c – Ya visitada
    if (fila, col) in visitados:
        return 0

    # PASO 2 – Marca como visitada
    visitados.add((fila, col))

    # PASO 3 – ¿Llegamos a la salida?
    if fila == filas-1 and col == cols-1:
        cantidad = 1
    else:
        cantidad = 0
        direcciones = [(1, 0), (0, 1), (-1, 0), (0, -1)]
        for df, dc in direcciones:
            cantidad += contar_caminos(laberinto, fila+df, col+dc, visitados)

    # PASO 4 – SIEMPRE backtrack
    visitados.discard((fila, col))

    # PASO 5 – return cantidad
    return cantidad


# ============================================================
# EXPERIMENTOS
# ============================================================

if __name__ == "__main__":

    print("=" * 50)
    print("PARTE 3A – Buscar un camino en LABERINTO_5x5")
    print("=" * 50)
    camino = encontrar_camino(LABERINTO_5x5, verbose=False)
    if camino:
        print(f" Camino encontrado ({len(camino)} pasos):")
        print(f" {camino}")
    else:
        print(" No existe camino.")

    print("\n" + "=" * 50)
    print("PARTE 3B – Visualización paso a paso (laberinto simple 3x3)")
    print("=" * 50)
    print(" (Activa verbose=True en encontrar_camino para ver cada paso)")
    camino_simple = encontrar_camino(LABERINTO_SIMPLE, verbose=True)
    if camino_simple:
        print(f"\n Camino final: {camino_simple}")

    print("\n" + "=" * 50)
    print("PARTE 3A – Laberinto sin salida")
    print("=" * 50)
    camino_ns = encontrar_camino(LABERINTO_SIN_SALIDA)
    if camino_ns is None:
        print(" Correctamente detectado: no existe camino. ✓")
    else:
        print(f" ERROR: debería ser None, se obtuvo {camino_ns}")

    print("\n" + "=" * 50)
    print("PARTE 3C – Contar todos los caminos")
    print("=" * 50)
    for nombre, lab in [("simple 3x3", LABERINTO_SIMPLE),
                        ("5x5 con paredes", LABERINTO_5x5)]:
        total = contar_caminos(lab, 0, 0, set())
        print(f" {nombre}: {total} camino(s)")

    print()
    print(" Reflexión: caminos_bottom_up(3,3) de la Parte 2 = 6 (solo abajo/derecha)")
    print(" contar_caminos(LABERINTO_SIMPLE) con 4 direcciones da 12.")
    print(" ¿Por qué son distintos? Escribe la respuesta en tu reporte.")
