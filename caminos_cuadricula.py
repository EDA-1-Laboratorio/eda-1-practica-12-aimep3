"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Parte 2 – Contando caminos en una cuadrícula

Instrucciones generales
    Implementa las funciones en el orden en que aparecen.
    Los comentarios guiados dentro de cada función te explican
    cómo razonar el problema paso a paso.
    Elimina los 'pass' conforme vayas completando cada función.

Ejecuta este archivo directamente para ver los resultados:
    python3 caminos_cuadricula.py
"""

import time


# ============================================================
# UTILIDAD DE MEDICIÓN (ya implementada — no modificar)
# ============================================================

def medir(funcion, *args, repeticiones: int = 5):
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
# PARTE 2A – CAMINOS SIN OBSTÁCULOS
# ============================================================
#
# CONTEXTO DEL PROBLEMA:
#   Un robot está en la celda (0, 0) de una cuadrícula de m × n.
#   Solo puede moverse HACIA ABAJO (fila + 1) o HACIA LA DERECHA (col + 1).
#   ¿Cuántos caminos distintos existen de (0,0) a (m-1, n-1)?
#
# ESTRUCTURA RECURSIVA — piensa en esto antes de codificar:
#   Para llegar a la celda (i, j), el robot debe haber venido de:
#       (i-1, j)  [un movimiento hacia abajo desde arriba]  O
#       (i, j-1)  [un movimiento hacia la derecha desde la izquierda]
#
#   Por tanto:  caminos(i, j) = caminos(i-1, j) + caminos(i, j-1)
#
#   CASOS BASE:
#   Si el robot está en la fila 0 (fila superior), solo puede haberse
#   movido hacia la derecha hasta llegar ahí → exactamente 1 camino.
#   Si está en la columna 0 (columna izquierda), solo pudo moverse
#   hacia abajo → exactamente 1 camino.
#   Por tanto:  caminos(0, j) = 1  para todo j
#               caminos(i, 0) = 1  para todo i


def caminos_recursivo(m: int, n: int) -> int:
    """
    Cuenta los caminos de (0,0) a (m-1, n-1) — versión recursiva.

    Parámetros:
        m – número de filas de la cuadrícula.
        n – número de columnas de la cuadrícula.

    CÓMO PENSARLO:
        Nota que la función recibe las DIMENSIONES de la cuadrícula,
        no las coordenadas actuales. Internamente, "caminos(m, n)"
        responde: ¿cuántos caminos hay para una cuadrícula de m×n?

        La recurrencia es equivalente a la que viste arriba:
            caminos(1, n) = 1  (solo hay una fila → solo moverse a la derecha)
            caminos(m, 1) = 1  (solo hay una columna → solo moverse hacia abajo)
            caminos(m, n) = caminos(m-1, n) + caminos(m, n-1)

        Imagina que "quitas" una fila (m-1) o una columna (n-1) y
        preguntas cuántos caminos quedan en la cuadrícula más pequeña.
    """
    # PASO 1 – Casos base.
    if m == 1 or n == 1:
        return 1

    # PASO 2 – Caso recursivo.
    return caminos_recursivo(m - 1, n) + caminos_recursivo(m, n - 1)


def caminos_memo(m: int, n: int, memo: dict = None) -> int:
    """
    Cuenta los caminos de (0,0) a (m-1, n-1) — versión memoización.

    CÓMO PENSARLO:
        El problema de la versión recursiva es que calcula los mismos
        sub-tableros muchas veces. Ejemplo para 4×4:
            caminos(4,3) y caminos(3,4) ambos necesitan caminos(3,3).
            caminos(3,3) se calcula dos veces.

        Usa un diccionario memo cuyas claves son tuplas (m, n).
        Antes de calcular caminos(m, n), revisa si (m, n) ya está en memo.

        La estructura es idéntica a fib_memo:
            1. Inicializa memo si es None.
            2. Casos base (devuelve 1 si m==1 o n==1).
            3. Revisa caché: if (m, n) in memo → return memo[(m, n)]
            4. Calcula recursivamente, guarda en memo[(m, n)], devuelve.
    """
    # 1. Inicializa memo si es None.
    if memo is None:
        memo = {}
        
    # 2. Casos base.
    if m == 1 or n == 1:
        return 1
        
    # 3. Revisa caché.
    if (m, n) in memo:
        return memo[(m, n)]
        
    # 4. Calcula recursivamente, guarda en memo y devuelve.
    memo[(m, n)] = caminos_memo(m - 1, n, memo) + caminos_memo(m, n - 1, memo)
    return memo[(m, n)]


def caminos_bottom_up(m: int, n: int) -> tuple:
    """
    Cuenta los caminos de (0,0) a (m-1, n-1) — versión tabulación.

    Retorna:
        (total_caminos: int, tabla: list[list[int]])
        La tabla completa se devuelve para poder visualizarla.

    CÓMO PENSARLO:
        Crea una matriz (lista de listas) de m filas × n columnas.
        Llénala en orden de fila por fila, columna por columna:

        INICIALIZACIÓN (casos base):
            Toda la primera fila:   tabla[0][j] = 1  para j en 0..n-1
            Toda la primera columna: tabla[i][0] = 1  para i en 0..m-1

        LLENADO (doble bucle):
            Para i de 1 a m-1:
                Para j de 1 a n-1:
                    tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]

        ¿Por qué este orden garantiza que tabla[i-1][j] y tabla[i][j-1]
        ya están calculados cuando llegamos a tabla[i][j]?
        (Pista: i-1 < i, y j-1 < j → ya los procesamos antes en el bucle.)

        Al terminar, la respuesta está en tabla[m-1][n-1].
    """
    # PASO 1 – Crea la tabla de m filas × n columnas llena de ceros.
    tabla = [[0] * n for _ in range(m)]

    # PASO 2 – Inicializa la primera fila.
    for j in range(n):
        tabla[0][j] = 1

    # PASO 3 – Inicializa la primera columna.
    for i in range(m):
        tabla[i][0] = 1

    # PASO 4 – Doble bucle de llenado (empieza en i=1, j=1).
    for i in range(1, m):
        for j in range(1, n):
            tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]

    # PASO 5 – Devuelve (tabla[m-1][n-1], tabla).
    return tabla[m-1][n-1], tabla


def imprimir_tabla(tabla: list, titulo: str = "Tabla DP") -> None:
    """
    Imprime la tabla DP con formato alineado.

    Ejemplo de salida para una cuadrícula 4×4:
        Tabla DP:
          1   1   1   1
          1   2   3   4
          1   3   6  10
          1   4  10  20

    CÓMO PENSARLO:
        Necesitas saber cuántos dígitos tiene el número más grande para
        alinear las columnas. Usa str(max_val) y len() para calcular
        el ancho de cada celda.

        Luego recorre fila por fila e imprime cada valor con ese ancho:
            print(" ".join(str(val).rjust(ancho) for val in fila))
    """
    # PASO 1 – Encuentra el valor máximo en toda la tabla.
    max_val = max(max(fila) for fila in tabla)
    ancho = len(str(max_val)) + 1   # (+ 1 para separación)

    # PASO 2 – Imprime el título.
    print(f"{titulo}:")

    # PASO 3 – Recorre las filas e imprime cada valor con rjust(ancho).
    for fila in tabla:
        print(" ".join(str(val).rjust(ancho) for val in fila))


# ============================================================
# PARTE 2B – CAMINOS CON OBSTÁCULOS
# ============================================================
#
# CONTEXTO:
#   Ahora la cuadrícula tiene celdas bloqueadas (valor 1 en el grid).
#   El robot NO puede pasar por esas celdas.
#
# CÓMO AFECTA ESTO A LA TABLA DP:
#   Una celda bloqueada tiene CERO caminos que pasen por ella.
#   Si grid[i][j] == 1  →  tabla[i][j] = 0
#
#   La inicialización de la primera fila y primera columna también cambia:
#   Si hay un obstáculo en la columna j de la primera fila, todas las
#   celdas (0, j), (0, j+1), ... son inaccesibles (0 caminos), porque
#   no hay otra forma de llegar a ellas.
#   Lo mismo aplica para la primera columna.


def caminos_con_obstaculos(grid: list) -> int:
    """
    Cuenta los caminos de (0,0) a (m-1, n-1) evitando obstáculos.

    Parámetros:
        grid – matriz de m × n donde 0 = libre, 1 = bloqueado.

    Retorna:
        Número de caminos válidos (0 si no existe ninguno).

    CÓMO PENSARLO:
        Sigue la misma estructura que caminos_bottom_up, pero con dos
        modificaciones:

        MODIFICACIÓN 1 – Inicialización de bordes con obstáculos:
            Primera fila: recorre j de izquierda a derecha.
                Si grid[0][j] == 1 → tabla[0][j] = 0, Y además todas las
                celdas (0, j+1), (0, j+2), ... también son 0 (usa break).
                Si grid[0][j] == 0 → tabla[0][j] = 1
            Primera columna: igual, pero por filas.

        MODIFICACIÓN 2 – Llenado interior:
            Si grid[i][j] == 1 → tabla[i][j] = 0 (sin sumar).
            Si grid[i][j] == 0 → tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]

        Caso especial: si la celda de inicio (0,0) o la de destino
        (m-1, n-1) está bloqueada, el resultado es 0 directamente.
    """
    # PASO 1 – Verifica si el inicio o el destino están bloqueados.
    m = len(grid)
    n = len(grid[0])
    
    if grid[0][0] == 1 or grid[m-1][n-1] == 1:
        return 0

    # PASO 2 – Crea la tabla de ceros.
    tabla = [[0] * n for _ in range(m)]

    # PASO 3 – Inicializa la primera fila considerando obstáculos.
    for j in range(n):
        if grid[0][j] == 1:
            break
        tabla[0][j] = 1

    # PASO 4 – Inicializa la primera columna considerando obstáculos.
    for i in range(m):
        if grid[i][0] == 1:
            break
        tabla[i][0] = 1

    # PASO 5 – Llena el interior (doble bucle desde i=1, j=1).
    for i in range(1, m):
        for j in range(1, n):
            if grid[i][j] == 1:
                tabla[i][j] = 0
            else:
                tabla[i][j] = tabla[i-1][j] + tabla[i][j-1]

    # PASO 6 – Retorna tabla[m-1][n-1].
    return tabla[m-1][n-1]


# ============================================================
# EXPERIMENTOS
# ============================================================

if __name__ == "__main__":

    # --- Verificación con casos conocidos ---
    print("=== Verificación de correctitud ===")
    casos = [(1, 1, 1), (2, 2, 2), (3, 3, 6), (3, 7, 28), (4, 4, 20)]
    for m, n, esperado in casos:
        r = caminos_recursivo(m, n)
        memo_r = caminos_memo(m, n)
        bu_result = caminos_bottom_up(m, n)
        bu = bu_result[0] if isinstance(bu_result, tuple) else bu_result
        ok = lambda v: "✓" if v == esperado else f"✗(esperado {esperado}, obtuvo {v})"
        print(f"  caminos({m}×{n}) = {esperado:4d}  recursivo:{ok(r)}  memo:{ok(memo_r)}  bottom_up:{ok(bu)}")

    # --- Visualización de la tabla ---
    print("\n=== Tabla DP para cuadrícula 5×5 ===")
    resultado_bu = caminos_bottom_up(5, 5)
    if isinstance(resultado_bu, tuple):
        total, tabla = resultado_bu
        imprimir_tabla(tabla, "Caminos 5×5")
        print(f"  Caminos totales: {total}")
    else:
        print("  (implementa caminos_bottom_up para ver la tabla)")

    # --- Experimento de tiempo ---
    print("\n=== Comparación de tiempos ===")
    print(f"{'cuadrícula':>12}  {'recursivo (s)':>16}  {'memo (s)':>12}  {'bottom_up (s)':>14}")
    for dim in [5, 10, 12, 15]:
        _, t_r = medir(caminos_recursivo, dim, dim)
        _, t_m = medir(caminos_memo, dim, dim)
        bu_fn = lambda d=dim: caminos_bottom_up(d, d)
        _, t_b = medir(bu_fn)
        print(f"  {dim:3d}×{dim:<3d}     {t_r:16.8f}  {t_m:12.8f}  {t_b:14.8f}")

    # --- Prueba con obstáculos ---
    print("\n=== Cuadrícula con obstáculos ===")
    grid_ejemplo = [
        [0, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 0, 1],
        [0, 0, 0, 0],
    ]
    print("  Grid:")
    for fila in grid_ejemplo:
        print("   ", fila)
    resultado_obs = caminos_con_obstaculos(grid_ejemplo)
    print(f"  Caminos evitando obstáculos: {resultado_obs}  (esperado: 4)")
