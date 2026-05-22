"""
Práctica 12 – Estrategias para la construcción de algoritmos II
Módulo  : Parte 1 – Fibonacci y Escalando Peldaños

Instrucciones generales
    Implementa cada función en el orden en que aparece.
    Cada bloque de comentarios guiados te explica CÓMO pensar el problema,
    no solo qué hacer. Léelos con cuidado antes de escribir código.
    Elimina los 'pass' conforme vayas completando cada función.

Ejecuta este archivo directamente para ver los resultados:
    python3 fibonacci_escaleras.py
"""

import time


# ============================================================
# UTILIDAD DE MEDICIÓN (ya implementada — no modificar)
# ============================================================

def medir(funcion, *args, repeticiones: int = 5):
    """
    Ejecuta funcion(*args) 'repeticiones' veces.
    Retorna (resultado, tiempo_promedio_en_segundos).
    """
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return resultado, sum(tiempos) / len(tiempos)


# ============================================================
# PARTE 1A – TRES VERSIONES DE FIBONACCI
# ============================================================

def fib_recursivo(n: int) -> int:
    """
    Calcula F(n) usando recursión directa.

    Retorna:
        El n-ésimo número de Fibonacci: F(0)=0, F(1)=1, F(2)=1, F(3)=2, ...

    CÓMO PENSARLO:
        La definición matemática ya es el algoritmo:
            F(0) = 0
            F(1) = 1
            F(n) = F(n-1) + F(n-2)  para n >= 2

        Tu función debe "traducir" esa definición directamente a Python.
        No uses bucles: la recursión ES la estructura de control.
    """
    # PASO 1 – Validación de entrada.
    #   ¿Qué pasa si alguien llama fib_recursivo(-3)?
    #   Lanza un ValueError con un mensaje que indique que n debe ser >= 0.
    #   Recuerda la sintaxis: raise ValueError("mensaje")

    # PASO 2 – Casos base.
    #   Son los valores de los que ya conoces la respuesta sin recurrir.
    #   F(0) = 0  →  retorna 0 directamente.
    #   F(1) = 1  →  retorna 1 directamente.
    #   Sin casos base, la recursión no termina nunca.

    # PASO 3 – Caso recursivo.
    #   Para n >= 2, la respuesta depende de dos subproblemas más pequeños.
    #   Escribe exactamente la fórmula matemática como código Python.
    #   No intentes optimizarla todavía; la claridad es el objetivo aquí.
    """
    Calcula F(n) usando recursión directa.
    """
    # PASO 1 – Validación de entrada.
    if n < 0:
        raise ValueError("n debe ser >= 0")

    # PASO 2 – Casos base.
    if n == 0:
        return 0
    if n == 1:
        return 1

    # PASO 3 – Caso recursivo.
    return fib_recursivo(n - 1) + fib_recursivo(n - 2)   


def fib_memo(n: int, memo: dict = None) -> int:
    """
    Calcula F(n) con recursión + memoización (top-down).

    Parámetros:
        n    – índice del número de Fibonacci.
        memo – diccionario compartido entre llamadas recursivas.
               Si es None, se crea uno nuevo. NO pongas {} como valor
               por defecto en la firma (antipatrón de Python: el dict
               mutable por defecto persiste entre llamadas).

    CÓMO PENSARLO:
        El problema de fib_recursivo es que recalcula los mismos n una y
        otra vez. La solución es recordar (memorizar) cada resultado la
        primera vez que se calcula.

        Piensa en el diccionario memo como una "caché":
            - Antes de calcular fib(n), pregunta: ¿ya está en memo?
            - Si SÍ  → devuelve memo[n] directamente (ahorra trabajo).
            - Si NO  → calcúlalo recursivamente, guárdalo en memo[n],
                       y luego devuélvelo.

        El orden de los pasos importa: primero revisa la caché, luego
        los casos base, luego el caso recursivo con guardado.
    """
    # PASO 1 – Inicialización del diccionario.
    #   Si memo es None, asígnale un diccionario vacío: memo = {}
    #   Esto asegura que todas las llamadas recursivas compartan el mismo dict.

    # PASO 2 – Validación de n (igual que en fib_recursivo).

    # PASO 3 – Casos base: F(0) = 0, F(1) = 1.
    #   Devuelve el valor directamente (no hace falta guardarlo en memo,
    #   aunque tampoco es incorrecto hacerlo).

    # PASO 4 – Revisión de caché.
    #   if n in memo: return memo[n]
    #   Si ya calculamos este valor antes, lo devolvemos sin recalcular.

    # PASO 5 – Caso recursivo con guardado.
    #   Calcula el resultado llamando recursivamente (igual que fib_recursivo),
    #   guárdalo en memo[n], y luego devuélvelo.
    #   En una sola línea: memo[n] = fib_memo(n-1, memo) + fib_memo(n-2, memo)
    #                      return memo[n]
    """
    Calcula F(n) con recursión + memoización (top-down).
    """
    # PASO 1 – Inicialización del diccionario.
    if memo is None:
        memo = {}

    # PASO 2 – Validación de n.
    if n < 0:
        raise ValueError("n debe ser >= 0")

    # PASO 3 – Casos base.
    if n == 0:
        return 0
    if n == 1:
        return 1

    # PASO 4 – Revisión de caché.
    if n in memo:
        return memo[n]

    # PASO 5 – Caso recursivo con guardado.
    memo[n] = fib_memo(n - 1, memo) + fib_memo(n - 2, memo)
    return memo[n]    


def fib_bottom_up(n: int) -> int:
    """
    Calcula F(n) con tabulación iterativa (bottom-up).

    CÓMO PENSARLO:
        La memoización (top-down) empieza desde el problema grande y
        desciende hacia los casos base. Bottom-up hace lo contrario:
        empieza desde los casos base y construye la solución ascendiendo.

        Piensa en una tabla (lista) de tamaño n+1:
            tabla[0] = 0   ← caso base
            tabla[1] = 1   ← caso base
            tabla[i] = tabla[i-1] + tabla[i-2]   para i de 2 a n

        El bucle llena la tabla de izquierda a derecha.
        Cuando llega a la posición n, la respuesta ya está calculada.

        Ventaja: no hay pila de llamadas recursivas → no hay riesgo de
        "RecursionError" para valores grandes de n.

        Optimización de espacio (opcional, para reflexionar):
        ¿Necesitas guardar TODA la tabla, o solo los dos últimos valores?
    """
    # PASO 1 – Validación de n.

    # PASO 2 – Casos base especiales.
    #   Si n == 0, retorna 0. Si n == 1, retorna 1.
    #   Sin esto, el bucle de abajo tendría problemas con índices.

    # PASO 3 – Crea la tabla: una lista de n+1 ceros.
    #   tabla = [0] * (n + 1)

    # PASO 4 – Inicializa los casos base en la tabla.
    #   tabla[0] = 0   (aunque ya es 0 por defecto)
    #   tabla[1] = 1

    # PASO 5 – Bucle de llenado de izquierda a derecha.
    #   for i in range(2, n + 1):
    #       tabla[i] = tabla[i-1] + tabla[i-2]

    # PASO 6 – Devuelve tabla[n].
    """
    Calcula F(n) con tabulación iterativa (bottom-up).
    """
    # PASO 1 – Validación de n.
    if n < 0:
        raise ValueError("n debe ser >= 0")

    # PASO 2 – Casos base especiales.
    if n == 0:
        return 0
    if n == 1:
        return 1

    # PASO 3 – Crea la tabla: una lista de n+1 ceros.
    tabla = [0] * (n + 1)

    # PASO 4 – Inicializa los casos base en la tabla.
    tabla[0] = 0
    tabla[1] = 1

    # PASO 5 – Bucle de llenado de izquierda a derecha.
    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]

    # PASO 6 – Devuelve tabla[n].
    return tabla[n]    


# ============================================================
# PARTE 1B – ESCALANDO PELDAÑOS
# ============================================================
#
# CONTEXTO DEL PROBLEMA:
#   Un robot sube una escalera de n peldaños. En cada turno sube
#   exactamente 1 o 2 peldaños. ¿De cuántas formas distintas puede
#   llegar al peldaño n?
#
# PISTA FUNDAMENTAL — antes de implementar, responde en papel:
#   - ¿De cuántas formas llega al peldaño 1?  (solo (1))         → 1 forma
#   - ¿De cuántas formas llega al peldaño 2?  ((1,1) y (2))      → 2 formas
#   - ¿De cuántas formas llega al peldaño 3?  ((1,1,1),(1,2),(2,1)) → 3 formas
#   - ¿De cuántas formas llega al peldaño 4?  (...)               → ? formas
#
#   Observa los números: 1, 2, 3, 5, ... ¿Los reconoces?
#
#   Ahora piensa RECURSIVAMENTE:
#   Para llegar al peldaño n, el robot debe haber estado en el peldaño
#   n-1 (y dar un paso de 1) O en el peldaño n-2 (y dar un salto de 2).
#   Por lo tanto:
#       escaleras(n) = escaleras(n-1) + escaleras(n-2)
#
#   ¡Es la misma recurrencia que Fibonacci! Solo cambian los casos base.


def escaleras_recursivo(n: int) -> int:
    """
    Cuenta las formas de subir n peldaños (1 o 2 a la vez) — versión recursiva.

    CÓMO PENSARLO:
        Una vez que identificaste que escaleras(n) = escaleras(n-1) + escaleras(n-2),
        los casos base son los que marcan la diferencia con Fibonacci:
            escaleras(0) = 1  (hay exactamente UNA forma de "subir" 0 peldaños:
                               no hacer nada — es la combinación vacía)
            escaleras(1) = 1
            escaleras(2) = 2
        Nota: algunos implementan solo escaleras(1)=1 y escaleras(2)=2,
        ignorando el caso n=0. Ambos enfoques son válidos si son consistentes.
    """
    # PASO 1 – Validación.
    #   Si n < 0, lanza ValueError.

    # PASO 2 – Casos base.
    #   n == 0 → 1 (convención: una forma de no moverse)
    #   n == 1 → 1
    #   n == 2 → 2  (puedes dejarlo en el caso recursivo si tus casos base
    #               son n=0 y n=1; comprueba que funcione antes de omitirlo)

    # PASO 3 – Caso recursivo: misma estructura que fib_recursivo.
    """
    Cuenta las formas de subir n peldaños (1 o 2 a la vez) — versión recursiva.
    """
    # PASO 1 – Validación.
    if n < 0:
        raise ValueError("n debe ser >= 0")

    # PASO 2 – Casos base.
    if n == 0:
        return 1
    if n == 1:
        return 1

    # PASO 3 – Caso recursivo.
    return escaleras_recursivo(n - 1) + escaleras_recursivo(n - 2)    


def escaleras_memo(n: int, memo: dict = None) -> int:
    """
    Cuenta las formas de subir n peldaños — versión con memoización.

    CÓMO PENSARLO:
        Sigue exactamente la misma estructura que fib_memo, pero con
        los casos base de escaleras_recursivo.
        La recurrencia es idéntica; lo único que cambia son esos casos base.
    """
    # Sigue los mismos pasos que fib_memo:
    # inicializa memo → valida n → casos base → revisa caché → recursivo+guardado.
    """
    Cuenta las formas de subir n peldaños — versión con memoización.
    """
    # Sigue los mismos pasos que fib_memo
    if memo is None:
        memo = {}

    if n < 0:
        raise ValueError("n debe ser >= 0")

    if n == 0:
        return 1
    if n == 1:
        return 1

    if n in memo:
        return memo[n]

    memo[n] = escaleras_memo(n - 1, memo) + escaleras_memo(n - 2, memo)
    return memo[n]    


def escaleras_bottom_up(n: int) -> int:
    """
    Cuenta las formas de subir n peldaños — versión tabulación iterativa.

    CÓMO PENSARLO:
        Misma estructura que fib_bottom_up, con los casos base de escaleras.
        tabla[0] = 1, tabla[1] = 1, tabla[2] = 2,
        tabla[i] = tabla[i-1] + tabla[i-2]  para i >= 3
        (o i >= 2 si tu caso base es solo tabla[0] y tabla[1]).
    """
    # Sigue la misma estructura que fib_bottom_up.
    """
    Cuenta las formas de subir n peldaños — versión tabulación iterativa.
    """
    # Sigue la misma estructura que fib_bottom_up
    if n < 0:
        raise ValueError("n debe ser >= 0")

    if n == 0:
        return 1
    if n == 1:
        return 1

    tabla = [0] * (n + 1)
    tabla[0] = 1
    tabla[1] = 1

    for i in range(2, n + 1):
        tabla[i] = tabla[i - 1] + tabla[i - 2]

    return tabla[n]    


# ============================================================
# EXPERIMENTOS — ejecuta este bloque para ver resultados
# ============================================================

if __name__ == "__main__":

    # --- Verificación de correctitud ---
    esperados_fib = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
    print("=== Verificación Fibonacci ===")
    for i, esperado in enumerate(esperados_fib):
        r = fib_recursivo(i)
        m = fib_memo(i)
        b = fib_bottom_up(i)
        ok_r = "✓" if r == esperado else f"✗(esperado {esperado}, obtuvo {r})"
        ok_m = "✓" if m == esperado else f"✗(esperado {esperado}, obtuvo {m})"
        ok_b = "✓" if b == esperado else f"✗(esperado {esperado}, obtuvo {b})"
        print(f"  F({i:2d}) = {esperado:4d}  recursivo:{ok_r}  memo:{ok_m}  bottom_up:{ok_b}")

    esperados_esc = [1, 1, 2, 3, 5, 8, 13, 21]
    print("\n=== Verificación Escaleras ===")
    for i, esperado in enumerate(esperados_esc):
        r = escaleras_recursivo(i)
        m = escaleras_memo(i)
        b = escaleras_bottom_up(i)
        ok_r = "✓" if r == esperado else f"✗(esperado {esperado}, obtuvo {r})"
        ok_m = "✓" if m == esperado else f"✗(esperado {esperado}, obtuvo {m})"
        ok_b = "✓" if b == esperado else f"✗(esperado {esperado}, obtuvo {b})"
        print(f"  esc({i}) = {esperado:4d}  recursivo:{ok_r}  memo:{ok_m}  bottom_up:{ok_b}")

    # --- Experimento de tiempo ---
    print("\n=== Comparación de tiempos: Fibonacci ===")
    print(f"{'n':>5}  {'recursivo (s)':>16}  {'memo (s)':>12}  {'bottom_up (s)':>14}")
    for n in [10, 20, 25, 30, 35]:
        _, t_r = medir(fib_recursivo, n)
        _, t_m = medir(fib_memo, n)
        _, t_b = medir(fib_bottom_up, n)
        print(f"  {n:3d}  {t_r:16.8f}  {t_m:12.8f}  {t_b:14.8f}")

    # --- Reflexión ---
    print("\n=== Escaleras vs Fibonacci ===")
    for n in range(1, 10):
        fib_n1 = fib_bottom_up(n + 1)
        esc_n  = escaleras_bottom_up(n)
        print(f"  escaleras({n}) = {esc_n:4d}   fib({n+1}) = {fib_n1:4d}  "
              f"{'¿iguales?' if esc_n == fib_n1 else 'DISTINTOS'}")
