"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Parte 4 – El problema de las N reinas

Instrucciones generales
    Lee con cuidado los comentarios de cada función. Esta parte introduce
    conceptos de teoría de la complejidad (P vs NP) a través de la
    distinción entre VERIFICAR una solución y ENCONTRARLA.
    Implementa las funciones en el orden en que aparecen.

Ejecuta este archivo directamente para ver los resultados:
    python3 n_reinas.py
"""

import time

# ============================================================
# REPRESENTACIÓN DEL TABLERO
# ============================================================
#
# Usamos una lista de N enteros:
#   tablero[i] = j  significa que la reina de la fila i está en la columna j.
#
# Esta representación garantiza que nunca habrá dos reinas en la misma fila
# (cada fila tiene exactamente una reina).
#
# Ejemplo para N=4, solución [1, 3, 0, 2]:
#
#   col →  0   1   2   3
#   fila 0: .   Q   .   .      tablero[0] = 1
#   fila 1: .   .   .   Q      tablero[1] = 3
#   fila 2: Q   .   .   .      tablero[2] = 0
#   fila 3: .   .   Q   .      tablero[3] = 2
#
# CONFLICTOS a detectar:
#   - Misma columna:  tablero[i] == tablero[j]
#   - Misma diagonal: |tablero[i] - tablero[j]| == |i - j|
#     (Las diagonales tienen pendiente ±1; si la diferencia de columnas
#      es igual a la diferencia de filas, las dos reinas se amenazan.)


# ============================================================
# PARTE 4A – EL VERIFICADOR (problema de verificación)
# ============================================================
#
# CONTEXTO P vs NP:
#   Este es el "verificador" del que se habla en el README.
#   Dada una configuración COMPLETA (tablero de N reinas ya colocadas),
#   decidir si es válida toma O(N²) — tiempo polinomial.
#   Esto es lo que hace a N-reinas estar en NP: podemos verificar
#   rápidamente si una solución candidata es correcta.

def es_valida(tablero: list) -> bool:
    """
    Verifica si un tablero COMPLETO es una solución válida al problema
    de las N reinas.

    Parámetros:
        tablero – lista de N enteros. tablero[i] = columna de la reina en fila i.
                  Se asume que el tablero está completamente lleno (N reinas).

    Retorna:
        True si ningún par de reinas se amenaza entre sí.
        False en cuanto se detecte algún conflicto.

    CÓMO PENSARLO:
        Necesitas revisar TODOS los pares de reinas (i, j) con i < j.
        Para cada par, verifica DOS condiciones:
            1. Misma columna:  tablero[i] == tablero[j]
            2. Misma diagonal: abs(tablero[i] - tablero[j]) == abs(i - j)

        Si CUALQUIERA se cumple → las reinas se amenazan → return False.
        Si NINGÚN par tiene conflicto → return True.

        Estructura con doble bucle anidado:
            for i in range(n):
                for j in range(i + 1, n):   ← solo pares distintos, sin repetir
                    if condición_1 or condición_2:
                        return False
            return True
    """
    n = len(tablero)

    # PASO 1 – Doble bucle sobre todos los pares (i, j) con i < j.
    for i in range(n):
        for j in range(i + 1, n):
            # PASO 2 – Verifica las dos condiciones de conflicto.
            #   Condición columna:  tablero[i] == tablero[j]
            #   Condición diagonal: abs(tablero[i] - tablero[j]) == abs(i - j)
            #   Si alguna se cumple, retorna False inmediatamente.
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                return False

    # PASO 3 – Si el bucle termina sin conflictos, retorna True.
    return True


# ============================================================
# PARTE 4B – VERIFICACIÓN INCREMENTAL EFICIENTE
# ============================================================
#
# CONTEXTO:
#   es_valida revisa TODO el tablero: O(N²).
#   Dentro del backtracking, colocamos reinas fila por fila de arriba
#   hacia abajo. Cuando vamos a colocar la reina en la fila 'fila',
#   las filas 0..(fila-1) ya tienen reinas colocadas.
#   Las filas fila+1..N-1 aún están vacías.
#
#   Solo necesitamos verificar si la nueva reina en (fila, col) conflicta
#   con las que ya están en las filas anteriores. Eso es O(N), no O(N²).
#
#   Esta eficiencia es lo que hace que el backtracking sea práctico.

def es_segura(tablero: list, fila: int, col: int) -> bool:
    """
    Verifica si colocar una reina en (fila, col) es seguro,
    dado que las filas 0..(fila-1) ya tienen reinas colocadas.

    Parámetros:
        tablero – lista de N enteros. Solo tablero[0..fila-1] son válidos;
                  tablero[fila..N-1] aún no están asignados (su valor no importa).
        fila    – índice de la fila donde queremos colocar la nueva reina.
        col     – columna propuesta para la nueva reina.

    Retorna:
        True si ninguna reina anterior amenaza a (fila, col).

    CÓMO PENSARLO:
        Itera i de 0 a fila-1 (las filas ya ocupadas).
        Para cada reina existente en (i, tablero[i]), verifica:
            1. Misma columna:  tablero[i] == col
            2. Misma diagonal: abs(tablero[i] - col) == abs(i - fila)

        Si cualquiera se cumple → return False.
        Si el bucle termina → return True.

        NOTA: No necesitas verificar la misma fila porque la representación
        garantiza que solo hay una reina por fila.
    """
    # Itera sobre las filas anteriores (0 a fila-1) y verifica conflictos.
    for i in range(fila):
        if tablero[i] == col or abs(tablero[i] - col) == abs(i - fila):
            return False
    return True


# ============================================================
# PARTE 4C – BACKTRACKING: ENCONTRAR UNA SOLUCIÓN
# ============================================================
#
# ESTRUCTURA DEL BACKTRACKING PARA N-REINAS:
#
#   El algoritmo coloca una reina por fila, de fila 0 a fila N-1.
#   En cada fila prueba cada columna de 0 a N-1.
#   Si la columna es segura (es_segura retorna True), la elige y avanza
#   recursivamente a la siguiente fila.
#   Si en alguna fila ninguna columna es segura, retrocede (backtrack).
#
#   ÁRBOL DE BÚSQUEDA para N=4:
#     fila 0: prueba col 0, 1, 2, 3
#       col 0 → fila 1: prueba col 0 (✗), 1 (✗), 2 (✓)...
#       col 1 → fila 1: prueba col 0 (✗), 1 (✗), 2 (✗), 3 (✓)...
#         ...
#
#   La PODA ocurre cuando es_segura retorna False: no exploramos esa
#   rama ni ninguna de sus subramas. Esto reduce enormemente el espacio.

def resolver_n_reinas(n: int, fila: int = 0,
                      tablero: list = None) -> list | None:
    """
    Encuentra la primera solución al problema de N reinas usando backtracking.

    Parámetros:
        n      – tamaño del tablero (N×N) y número de reinas.
        fila   – fila actual que estamos intentando ocupar (empieza en 0).
        tablero – lista de N enteros que se va llenando. Si es None, se crea.

    Retorna:
        Lista de N enteros (tablero completo) con la primera solución, o
        None si no existe ninguna solución.

    CÓMO PENSARLO:
        CASO BASE (éxito):
            Si fila == n, todas las reinas están colocadas → retorna tablero.copy()
            (copiamos para no retornar una referencia que se modifique después)

        CASO RECURSIVO:
            for col in range(n):
                if es_segura(tablero, fila, col):
                    tablero[fila] = col            ← coloca la reina
                    resultado = resolver_n_reinas(n, fila+1, tablero)
                    if resultado is not None:
                        return resultado           ← propagamos la solución
                    tablero[fila] = -1             ← backtrack: quita la reina

            Si ninguna columna funcionó → return None (esta rama no tiene solución)

        La primera llamada es: resolver_n_reinas(n, 0, [-1]*n)
    """
    # PASO 1 – Inicialización del tablero (solo en la primera llamada).
    if tablero is None:
        tablero = [-1] * n

    # PASO 2 – Caso base de éxito.
    if fila == n:
        return tablero.copy()

    # PASO 3 – Caso recursivo: prueba cada columna de 0 a n-1.
    #   Para cada col, verifica es_segura → coloca → recursa → backtrack.
    for col in range(n):
        if es_segura(tablero, fila, col):
            tablero[fila] = col
            resultado = resolver_n_reinas(n, fila + 1, tablero)
            if resultado is not None:
                return resultado
            tablero[fila] = -1

    # PASO 4 – Si ninguna columna funcionó, retorna None.
    return None


def imprimir_tablero(tablero: list, titulo: str = "Tablero") -> None:
    """
    Imprime el tablero de ajedrez con las posiciones de las reinas.

    Leyenda:
        Q  → reina
        .  → celda vacía

    Ejemplo para tablero = [1, 3, 0, 2]:
        Tablero:
        . Q . .
        . . . Q
        Q . . .
        . . Q .

    CÓMO PENSARLO:
        Recorre cada fila i.
        En cada fila, recorre cada columna j.
        Si tablero[i] == j → imprime 'Q', de lo contrario '.'
        Separa las celdas con espacios.
    """
    n = len(tablero)
    print(f"\n{titulo}:")
    # Para cada fila, construye una cadena con 'Q' en la columna correspondiente.
    # Usa " ".join(...) para separar con espacios.
    for i in range(n):
        fila_actual = []
        for j in range(n):
            if tablero[i] == j:
                fila_actual.append("Q")
            else:
                fila_actual.append(".")
        print(" ".join(fila_actual))


# ============================================================
# PARTE 4D – CONTAR TODAS LAS SOLUCIONES
# ============================================================
#
# La estructura es casi idéntica a resolver_n_reinas, pero:
#   - En lugar de retornar la primera solución, CONTAMOS cada éxito.
#   - NUNCA retornamos al encontrar una solución; seguimos explorando.
#   - Siempre hacemos backtrack (tablero[fila] = -1) al terminar cada rama.

def contar_soluciones(n: int, fila: int = 0,
                      tablero: list = None) -> int:
    """
    Cuenta todas las soluciones al problema de N reinas.

    Retorna:
        Número entero con la cantidad de soluciones distintas.

    CÓMO PENSARLO:
        CASO BASE:
            Si fila == n → encontramos una solución completa → return 1

        CASO RECURSIVO:
            count = 0
            for col in range(n):
                if es_segura(tablero, fila, col):
                    tablero[fila] = col
                    count += contar_soluciones(n, fila+1, tablero)   ← SUMA (no retorna)
                    tablero[fila] = -1   ← siempre backtrack

            return count

        Observa la diferencia clave: no retornamos al primer éxito,
        sino que ACUMULAMOS el conteo de todas las ramas.
    """
    # PASO 1 – Inicialización del tablero.
    if tablero is None:
        tablero = [-1] * n

    # PASO 2 – Caso base.
    if fila == n:
        return 1

    # PASO 3 – Caso recursivo: itera columnas, acumula count.
    count = 0
    for col in range(n):
        if es_segura(tablero, fila, col):
            tablero[fila] = col
            count += contar_soluciones(n, fila + 1, tablero)
            tablero[fila] = -1

    # PASO 4 – return count
    return count


# ============================================================
# PARTE 4E – ANÁLISIS DE COMPLEJIDAD
# ============================================================

def medir(funcion, *args, repeticiones: int = 3):
    """Ejecuta funcion(*args) 'repeticiones' veces. Retorna (resultado, t_promedio)."""
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return resultado, sum(tiempos) / len(tiempos)


# ============================================================
# EXPERIMENTOS
# ============================================================

if __name__ == "__main__":

    # --- Verificación de es_valida ---
    print("=== Verificación de es_valida ===")
    valida_4    = [1, 3, 0, 2]   # solución conocida para N=4
    invalida_4  = [0, 0, 0, 0]   # cuatro reinas en la misma columna
    invalida_d  = [0, 1, 2, 3]   # diagonal
    print(f"  [1,3,0,2] válida:  {es_valida(valida_4)}   (esperado: True)")
    print(f"  [0,0,0,0] válida:  {es_valida(invalida_4)} (esperado: False)")
    print(f"  [0,1,2,3] válida:  {es_valida(invalida_d)} (esperado: False)")

    # --- Primera solución para varios N ---
    print("\n=== Primera solución por N ===")
    for n in range(1, 9):
        sol = resolver_n_reinas(n)
        if sol:
            print(f"  N={n}: {sol}")
            # Verifica con el verificador del Problema 4A
            check = "✓ (es_valida)" if es_valida(sol) else "✗ (es_valida FALLA)"
            print(f"        {check}")
        else:
            print(f"  N={n}: No existe solución")

    # --- Visualización de una solución ---
    sol_8 = resolver_n_reinas(8)
    if sol_8:
        imprimir_tablero(sol_8, "Solución para N=8")

    # --- Conteo de soluciones ---
    print("\n=== Conteo de soluciones ===")
    print(f"{'N':>4}  {'Soluciones':>12}  {'Tiempo (s)':>12}")
    for n in range(1, 13):
        count, t = medir(contar_soluciones, n)
        print(f"  {n:2d}  {count:12d}  {t:12.6f}")

    # --- Test de doblamiento para contar_soluciones ---
    print("\n=== Test de doblamiento (contar_soluciones) ===")
    tiempos = {}
    for n in [4, 6, 8, 10, 12]:
        _, t = medir(contar_soluciones, n)
        tiempos[n] = t
    ns_pares = [(4, 8), (6, 10), (8, 12)]
    print(f"  {'n':>4}  {'T(n)':>12}  {'T(n+4)':>12}  {'r = T(n+4)/T(n)':>18}")
    for n_a, n_b in ns_pares:
        r = tiempos[n_b] / tiempos[n_a] if tiempos[n_a] > 0 else float('inf')
        print(f"  {n_a:4d}  {tiempos[n_a]:12.6f}  {tiempos[n_b]:12.6f}  {r:18.2f}")
