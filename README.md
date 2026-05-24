[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/hFIMp7Y-)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=23986840&assignment_repo_type=AssignmentRepo)
# Práctica 12 - Estrategias para la construcción de algoritmos II

## Base documental
Esta práctica integra los conceptos estudiados en las últimas semanas del semestre: recursión, memoización (top-down), tabulación (bottom-up) y backtracking. El hilo conductor es la pregunta: **¿cómo puede un algoritmo explorar un espacio de soluciones de forma inteligente?**

## Objetivo general
Dominar la transición entre tres estrategias de cómputo que comparten la idea de **dividir un problema en subproblemas**:

- **Recursión directa** — solución limpia pero potencialmente exponencial si los subproblemas se traslapan.
- **Programación dinámica** — recursión + memoria (memoización o tabla) que convierte soluciones exponenciales en polinomiales cuando los subproblemas se repiten.
- **Backtracking** — exploración exhaustiva del espacio de soluciones que prune (poda) caminos inválidos en cuanto se detectan, sin necesidad de explorarlos completos.

## Sesión de clase relacionada
En las semanas previas se estudió el cálculo del n-ésimo número de Fibonacci con tres estrategias:
1. **Versión recursiva** — elegante pero con complejidad O(2ⁿ) por subproblemas traslapados.
2. **Top-down (memoización)** — se agrega un diccionario `memo` para guardar resultados ya calculados; primera llamada costosa, llamadas posteriores O(1).
3. **Bottom-up (tabulación)** — se llena una tabla iterativamente de los casos base hacia arriba; O(n) en tiempo y espacio.

Esta práctica usa ese conocimiento como punto de partida y lo extiende hacia problemas de mayor complejidad estructural.

## Competencias a desarrollar
Al finalizar la práctica, el equipo será capaz de:

- Identificar la estructura de subproblemas traslapados y subestructura óptima en un problema.
- Implementar las tres versiones (recursiva, top-down, bottom-up) de forma independiente para un problema dado.
- Diseñar un algoritmo de backtracking que explore un espacio de búsqueda y retroceda (poda) cuando un camino no puede llevar a la solución.
- Visualizar la ejecución del backtracking para entender cómo la pila de llamadas representa el estado de la búsqueda.
- Distinguir entre el **problema de búsqueda** y el **problema de verificación**, y relacionar esta distinción con las clases de complejidad P y NP.

## Requisitos técnicos
- Python 3.10 o superior.
- Bibliotecas permitidas: `time`, `sys`, `copy`. No se permite `functools.lru_cache` ni ninguna librería que implemente memoización automáticamente (el objetivo es implementarla manualmente).
- Entorno sugerido: VS Code con terminal integrada.

## Entregables
- Código fuente organizado en los cuatro módulos de esta práctica.
- Reporte técnico breve (4 a 8 páginas) con metodología, tablas de medición, respuestas a las preguntas de reflexión y conclusiones.
- Evidencia de ejecución (capturas o bitácora de terminal) que muestre la visualización del backtracking.

## Estructura de archivos
```
recursion_dinamica/
  fibonacci_escaleras.py       ← Parte 1 (entregar con TODO resueltos)
  caminos_cuadricula.py        ← Parte 2
  laberinto.py                 ← Parte 3
  n_reinas.py                  ← Parte 4
```

---

## Parte 0. Herramientas de medición reutilizables

Antes de empezar, estudia este fragmento que usarás a lo largo de la práctica para medir el tiempo de cualquier función:

```python
import time

def medir(funcion, *args, repeticiones=5):
    """
    Ejecuta 'funcion(*args)' un número de veces y devuelve
    (resultado, tiempo_promedio_en_segundos).
    Tomar el promedio reduce el ruido del sistema operativo.
    """
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        inicio = time.perf_counter()
        resultado = funcion(*args)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return resultado, sum(tiempos) / len(tiempos)
```

### Test de doblamiento
Para estimar la complejidad empírica, ejecuta el algoritmo con tamaños n, 2n, 4n, … y calcula la razón:

$$r(n) = \frac{T(2n)}{T(n)}$$

| r aproximado | Clase estimada |
|:---:|:---|
| ≈ 1 | O(1) |
| ≈ 2 | O(n) |
| ≈ 4 | O(n²) |
| crece sin límite | O(kⁿ) – exponencial |

---

## Parte 1. Fibonacci y "Escalando peldaños"

### Marco teórico

La sucesión de Fibonacci define cada término en función de los dos anteriores:

$$F(0) = 0, \quad F(1) = 1, \quad F(n) = F(n-1) + F(n-2) \quad \text{para } n \geq 2$$

La versión recursiva directa tiene complejidad **O(2ⁿ)** porque recalcula los mismos subproblemas múltiples veces. El árbol de llamadas de `fib(5)` ilustra el desperdicio:

```
                    fib(5)
                  /        \
            fib(4)           fib(3)
           /      \         /      \
       fib(3)   fib(2)  fib(2)   fib(1)
       /    \
   fib(2) fib(1)
```

`fib(3)` se calcula dos veces; `fib(2)` se calcula tres veces. La memoización elimina este desperdicio almacenando cada resultado la primera vez que se calcula.

### Descubrimiento guiado — respondan en equipo antes de codificar

1. En el árbol de llamadas de `fib(6)`, ¿cuántas veces se calcula `fib(2)`? ¿Y `fib(3)`? Dibuja el árbol completo.
2. Si un equipo lleva un registro (diccionario) de los resultados ya calculados, ¿cuántas llamadas reales necesitaría `fib_memo(6)` la *primera* vez? ¿Y la *segunda* vez que se llama con n=6?
3. En la versión bottom-up, ¿en qué orden se llenan las celdas de la tabla? ¿Por qué ese orden garantiza que cuando calculas `tabla[i]` ya tienes disponibles `tabla[i-1]` y `tabla[i-2]`?
4. ¿Cuántas formas hay de subir 1 peldaño? ¿Y 2 peldaños? ¿Y 3 peldaños, si en cada paso puedes subir 1 o 2 a la vez? Escribe los primeros cinco valores. ¿Reconoces el patrón?

### Problema 1A — Tres versiones de Fibonacci (archivo: `fibonacci_escaleras.py`)

Implementa `fib_recursivo`, `fib_memo` y `fib_bottom_up`. Consulta los comentarios guiados dentro del archivo para saber exactamente cómo razonar cada paso.

Después de implementar, ejecuta el siguiente experimento y llena la tabla:

| n | T recursivo (s) | T memo (s) | T bottom-up (s) |
|---:|---:|---:|---:|
| 10 | 0.00001500     | 0.00000300 | 0.00000200 |
| 20 | 0.0018000      | 0.00000600 | 0.00000400 |
| 30 | 0.22000000     | 0.00000900 | 0.00000600 |
| 35 | 2.45000000     | 0.00001100 | 0.00000700 |

**Preguntas de análisis:**
- ¿A partir de qué valor de n el tiempo recursivo se vuelve notablemente mayor? n=30 o n=35
- Aplica el test de doblamiento al tiempo recursivo: ¿qué razón r(n) obtienes? r(n)= T(n)/T(n-1)
- Compara la razón con la tabla del Marco metodológico. ¿Qué clase de complejidad te sugiere? Complejidad exponencial, se simplifica como 0(2^n)

### Problema 1B — Escalando peldaños

Un robot puede subir una escalera de n peldaños. En cada turno sube exactamente **1 o 2 peldaños**. ¿De cuántas formas distintas puede llegar al peldaño n?

Por ejemplo: para n=3, las formas son (1,1,1), (1,2), (2,1) → **3 formas**.

Implementa `escaleras_recursivo`, `escaleras_memo` y `escaleras_bottom_up` en el mismo archivo.

**Preguntas de reflexión:**
- ¿Cuál es la recurrencia matemática de este problema? Escríbela formalmente. escaleras (n)= {1 si n=0,1 si n = 1, escaleras (n-1) + escaleras(n-2)   si 2≤n
- ¿En qué se parece a Fibonacci? ¿En qué difiere exactamente (valores de los casos base)? Se parece en su estructura. Para resol el problema de tamaño n y necesitas sumar los resultados de los dos subproblemas inmediatamente anteriores.
- Si el robot también pudiera subir 3 peldaños en un turno, ¿cómo cambiaría la recurrencia? Para 1 peldaño: 1 forma (1). Para 2 peldaños: 2 formas (1,1 y 2). Para 3 peldaños 4 formas (1,1,1; 1,2; 2,1 y 3).

---

## Parte 2. Contando caminos en una cuadrícula

### Marco teórico

Un robot se encuentra en la celda (0, 0) de una cuadrícula de m filas × n columnas. Solo puede moverse **hacia abajo** (incrementa fila) o **hacia la derecha** (incrementa columna). ¿Cuántos caminos distintos existen de (0,0) a (m−1, n−1)?

La estructura recursiva surge de preguntarse: para llegar a la celda (i, j), ¿desde dónde pudo venir el robot? Solo pudo venir de (i−1, j) o de (i, j−1). Por tanto:

$$\text{caminos}(i, j) = \text{caminos}(i-1, j) + \text{caminos}(i, j-1)$$

¿Cuáles son los casos base? Cualquier celda de la primera fila (i=0) o la primera columna (j=0) solo tiene **un** camino para llegar a ella (siempre moviéndose en una sola dirección).

### Descubrimiento guiado

1. Calcula a mano cuántos caminos hay en una cuadrícula 3×3. Dibuja todos los caminos posibles.
RRDD
RDRD
RDDR
DRRD
DRDR
DDRR
2. Llena la siguiente tabla con los valores de `caminos(m, n)` para m, n ∈ {1, 2, 3, 4, 5}:

   |   | n=1 | n=2 | n=3 | n=4 | n=5 |
   |---|---|---|---|---|---|
   | **m=1** |1 |1 |1 |1 |1 |
   | **m=2** |1 |2 |3 |4 |5 |
   | **m=3** |1 |3 |6 |10 |15 |
   | **m=4** |1 |4 |10 |20 |35 |
   | **m=5** |1 |5 |15 |35 |70 |

3. ¿Reconoces el patrón? ¿Qué famosa estructura matemática aparece en la tabla?
La estructura que se forma es el Triángulo de Pascal, que se puede ver claramente a la hora de voltear el cuadrado 45° y con eso podemos observar como la suma de los números vecinos forman el que le sigue hacia abajo.
4. Ahora agrega un obstáculo: la celda (1,1) está bloqueada. ¿Cuántos caminos quedan para una cuadrícula 3×3? Razona sin código primero.
Ya que los caminos totales son 6 (y ya los tenemos), podemos deducir fácil que hay 4 caminos que pasan por la celda (1,1) y por ende solo hacemos la resta de 6-4=2 y es el total de caminos posibles que no pasan por la casilla de (1,1).
### Problema 2A — Versiones sin obstáculos (archivo: `caminos_cuadricula.py`)

Implementa `caminos_recursivo`, `caminos_memo` y `caminos_bottom_up`. La versión bottom-up devuelve **tanto el resultado como la tabla completa** para poder imprimirla.

Implementa también `imprimir_tabla(tabla)` para visualizar la tabla DP con formato alineado.

### Problema 2B — Con obstáculos

Implementa `caminos_con_obstaculos(grid)` donde `grid` es una matriz de 0s y 1s (1 = obstáculo). El robot no puede pasar por celdas con valor 1.

**Pista clave:** si `grid[i][j] == 1`, entonces `tabla[i][j] = 0` (ningún camino puede pasar por ahí). Ajusta también la inicialización de la primera fila y primera columna: si hay un obstáculo en la fila 0 en la columna j, todas las celdas (0, j'), (0, j''+1), … también son inaccesibles.

**Preguntas de análisis:**
- Compara el tiempo de `caminos_recursivo` y `caminos_bottom_up` para una cuadrícula 15×15. Aplica el test de doblamiento.
Para la cuadrícula de 15x15, el algoritmo "caminos_recursivo" tardó 6.36879640 segundos, mientras que el "caminos_bottom_up" tardó apenas 0.00002954 segundos.
   Bottom-Up: El factor al dividir la 10x10 entre la 5x5 (el doble) es de 5.312977099, esto nos demuestra que su crecimiento es controlable y proporcional al tamaño de la tabla, a un factor cercano a 4 como lo esperabamos.
   Recursivo: En este caso, el problema simplemente explota, ya que contrario al caso anterior, en este el factor es de 1465.446097, lo cual nos demuestra que para el algoritmo recursivo, se comienza a poner peor entre más aumentemos el orden de nuestra matriz.
- ¿Por qué la versión bottom-up no necesita recursión ni pila de llamadas? ¿Qué ventaja práctica tiene eso en lenguajes con límite de profundidad de pila?
Bottom-up no necesita recursión porque este no construye la solución basandose en la pregunta de "de donde viene esto?", si no que lo que hace es construir la solución desde casos bases o sencillos y asi ir llegando a la solución poco a poco, lo que no obliga a estar llamando a la función cada vez que se quiera hacer o continuar al siguiente paso.
La ventaja de bottom-up es que al usar arreglos y ciclos en lugar de apilar funciones, esto hace que se consuma muy poca memoria y esto es lo que se busca para que no se llegue a un límite en la recursión y no lleguemos a un error en el programa por falta de memoria.

---

## Parte 3. El ratón en el laberinto

### Marco teórico

En los problemas anteriores **contábamos** caminos; aquí queremos **encontrar** uno (o saber si existe). Esta distinción es fundamental: contar tiene estructura DP porque acumulamos resultados de subproblemas independientes, pero *encontrar un camino específico* requiere explorar, tomar decisiones y, si llegamos a un callejón sin salida, **retroceder** (backtrack).

El backtracking es recursión que:
1. **Elige** una acción (moverse a una celda vecina).
2. **Explora** recursivamente desde la nueva posición.
3. **Deshace** la acción (backtrack) si la exploración no condujo a la solución.

La visualización del proceso es esencial: al imprimir el estado del laberinto en cada llamada, se observa literalmente cómo la recursión "avanza" y "retrocede".

### Representación del laberinto

```
0 = celda libre
1 = pared (no transitable)
'S' = celda de inicio (0,0)
'E' = celda de salida (n-1, m-1)
'·' = celda en la ruta actual
'✗' = celda intentada pero descartada (backtrack)
```

Ejemplo de laberinto 5×5:
```python
laberinto = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0],
]
```

### Descubrimiento guiado

1. Traza a mano el laberinto del ejemplo anterior en papel cuadriculado. Intenta encontrar un camino de (0,0) a (4,4) moviéndote solo vertical u horizontalmente.
2. ¿Cuántos caminos distintos existen en ese laberinto?
3. Imagina que eres el algoritmo de backtracking. Describe en palabras el momento exacto en que "retrocedes": ¿qué condición lo desencadena?
4. ¿Por qué es necesario llevar un registro de celdas "ya visitadas"? ¿Qué pasaría si no lo hicieras?

### Problema 3A — Backtracking básico (archivo: `laberinto.py`)

Implementa `existe_camino(laberinto, fila, col, visitados, ruta)`. La función devuelve `True` si encontró un camino (modificando `ruta` con las celdas del camino) o `False` si no existe.

### Problema 3B — Visualización del backtracking

Implementa `imprimir_laberinto(laberinto, visitados, ruta)` que imprime el estado actual del laberinto con los símbolos descritos arriba. Llama a esta función **dentro** de la función recursiva para observar el progreso.

Ejecuta el algoritmo en el laberinto de ejemplo y observa la salida. Escribe en el reporte una descripción de lo que ves: ¿cuántas veces se retrocede? ¿En qué celdas ocurre el backtrack?

### Problema 3C — Contando todos los caminos

Implementa `contar_caminos(laberinto, fila, col, visitados)`. A diferencia de la versión anterior, esta **no se detiene** al encontrar el primero, sino que sigue explorando para contar todos los caminos válidos.

**Preguntas de reflexión:**
- En el Problema 2 (sin obstáculos) el conteo tenía estructura DP. En este problema (con paredes) también cuenta. ¿Puedes escribir la versión DP de `contar_caminos`? ¿Qué diferencia hay con la versión backtracking?
- ¿Por qué la versión backtracking para *contar* todos los caminos tiene que "desvisitar" celdas al retroceder, mientras que la versión para *encontrar* uno puede dejar las celdas marcadas como visitadas permanentemente?

---

## Parte 4. El problema de las N reinas

### Marco teórico: búsqueda, verificación y las clases P y NP

El problema de las **N reinas** consiste en colocar N reinas en un tablero de ajedrez N×N de forma que **ninguna reina amenace a otra** (no compartan fila, columna ni diagonal).

Antes de programar nada, considera esta pregunta aparentemente simple: **¿cómo sabes si una configuración dada *es* una solución válida?**

Para responderla, distinguiremos dos problemas:

#### El problema de verificación
Dado un tablero con N reinas ya colocadas, **verificar** si la configuración es válida es sencillo:
- Revisa cada par de reinas (i, j).
- Si comparten columna: inválido.
- Si comparten diagonal: inválido.
- Si ningún par viola las reglas: válido.

Este proceso toma **O(N²)** operaciones — tiempo polinomial en N. Un verificador tan eficiente existe para todos los problemas de la clase **NP**: dada una solución candidata, puedes comprobar su validez rápidamente.

#### El problema de búsqueda
**Encontrar** una configuración válida es mucho más costoso si lo intentamos ingenuamente:
- Hay N² posiciones en el tablero.
- Queremos elegir N de ellas para las reinas.
- El número de combinaciones es $\binom{N^2}{N}$, que crece explosivamente.

El backtracking reduce drásticamente ese espacio: en lugar de generar todas las combinaciones y luego verificar, **poda** ramas del árbol de búsqueda en cuanto detecta que una colocación parcial ya viola las reglas.

#### La pregunta P vs NP
La pregunta central de la teoría de la complejidad computacional es:

> **¿Todo problema cuya solución puede verificarse eficientemente también puede resolverse eficientemente?**

Formalmente: ¿P = NP?

- La clase **P** contiene los problemas que se pueden *resolver* en tiempo polinomial.
- La clase **NP** contiene los problemas cuya solución puede *verificarse* en tiempo polinomial.
- Claramente P ⊆ NP (si puedes resolver algo rápido, también puedes verificarlo rápido).
- La pregunta abierta es si NP ⊆ P, es decir, si todo lo que se verifica rápido también se puede *encontrar* rápido.

El problema de las N reinas en sí **pertenece a P** (existen algoritmos O(N) que encuentran *una* solución). Lo valioso de este ejemplo es que la versión *conteo* (¿cuántas soluciones distintas existen?) no tiene solución polinomial conocida para N general. Y la estructura verificar-vs-buscar que acabas de ver es exactamente la asimetría que motiva la pregunta P vs NP.

### Representación del tablero

Usaremos una lista `tablero` de N enteros donde `tablero[i]` indica en qué **columna** está la reina de la fila i. Esto garantiza automáticamente que no hay dos reinas en la misma fila.

```python
# Ejemplo de solución para N=4:
tablero = [1, 3, 0, 2]
# Reina en fila 0 → columna 1
# Reina en fila 1 → columna 3
# Reina en fila 2 → columna 0
# Reina en fila 3 → columna 2
```

Visualización:
```
. Q . .
. . . Q
Q . . .
. . Q .
```

### Descubrimiento guiado

1. Para N=4, intenta encontrar a mano una configuración válida. ¿Cuántos intentos necesitaste?
2. Con la representación de lista `tablero[i] = columna`, ¿qué condición matemática expresa que las reinas en las filas `i` y `j` están en la misma columna?
3. La condición de diagonal es más sutil. Dos celdas (i, col_i) y (j, col_j) están en la misma diagonal si y solo si $|col_i - col_j| = |i - j|$. ¿Por qué? Dibuja un tablero 4×4 y verifica con un par de ejemplos.
4. El algoritmo de backtracking para N reinas coloca una reina por fila, de arriba hacia abajo. Antes de colocar la reina en la fila `fila`, solo necesita verificar contra las filas `0` a `fila-1` (las siguientes aún no tienen reina). ¿Por qué esto es una ventaja respecto a usar el verificador O(N²) completo en cada paso?

### Problema 4A — Verificador (archivo: `n_reinas.py`)

Implementa `es_valida(tablero)`: dado un tablero **completo** (N reinas ya colocadas), devuelve `True` si ninguna reina amenaza a otra.

Este es el **verificador** que discutimos arriba. Confirma que tiene complejidad O(N²).

### Problema 4B — Verificación incremental eficiente

Implementa `es_segura(tablero, fila, col)`: dado un tablero **parcialmente lleno** (reinas en filas 0..fila-1) y una posición propuesta `(fila, col)`, devuelve `True` si colocar una reina ahí no conflicta con ninguna reina ya colocada.

Esta función se usará dentro del backtracking para podar el árbol de búsqueda. Asegúrate de que sea O(N) (no O(N²)).

### Problema 4C — Backtracking: encontrar una solución

Implementa `resolver_n_reinas(n)` usando backtracking. La función devuelve la lista `tablero` con la primera solución encontrada, o `None` si no existe solución.

Implementa también `imprimir_tablero(tablero)` para visualizar la solución en formato tablero de ajedrez.

Prueba tu solución para N = 1, 2, 3, 4, 5, 6, 7, 8. ¿Para cuáles no existe solución? Para N=2 y N=3

### Problema 4D — Contando todas las soluciones

Implementa `contar_soluciones(n)` que devuelve cuántas configuraciones válidas existen para N reinas.

Llena la siguiente tabla:

| N | Soluciones |
|---:|---:|
| 1 | 1 |
| 2 | 0 |
| 3 | 0 |
| 4 | 2 |
| 5 | 10 |
| 6 | 4 |
| 7 | 40 |
| 8 | 92 |

La secuencia resultante es conocida en matemáticas. Búscala en [OEIS A000170](https://oeis.org/A000170).

### Problema 4E — Análisis de complejidad

Mide el tiempo de `contar_soluciones(n)` para n = 4, 6, 8, 10, 12 y aplica el test de doblamiento.

**Preguntas de reflexión:**
- ¿Qué razón r(n) observas? ¿A qué clase de complejidad corresponde?
  Observo que la razón r(n) no es constante, sino que crece de forma acelerada con cada incremento (pasando de aproximadamente 300, a 670, y luego a 939 según los datos). Si el algoritmo tuviera una complejidad polinomial, esta razón tendería a estabilizarse o decrecer. El hecho de que la razón se dispare indica que el algoritmo pertenece a una clase de complejidad exponencial (O(c^N)) o factorial (O(N!)). 

- El backtracking poda ramas inválidas. Si *no* hicieras ninguna poda (generaras todas las permutaciones y luego verificaras con `es_valida`), ¿cuántas configuraciones tendrías que verificar para N=8? (Pista: el número de permutaciones de 8 elementos es 8!).
  Si generamos todas las permutaciones garantizando únicamente que no se repitan filas ni columnas (pero sin verificar las diagonales tempranamente), tendríamos que calcular el factorial de 8. La operación es: 8! = 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 = 40,320 configuraciones. 

- Compara ese número con la cantidad de nodos que realmente visita el backtracking con poda. ¿Por qué la poda hace una diferencia tan grande?
  El número de 40,320 configuraciones es abismalmente mayor que los nodos que visita el backtracking (el cual solo llega hasta el final en las 92 soluciones correctas y unas cuantas ramas cercanas). 
La poda hace una diferencia gigantesca porque elimina ramas completas desde la raíz. Si el algoritmo coloca la reina de la fila 0 y la reina de la fila 1 y detecta que ya se atacan en diagonal, detiene esa búsqueda de inmediato. Al hacer esto, se ahorra generar y verificar las 6! = 720 combinaciones posibles que existirían para las filas restantes debajo de ese error. 

- Retoma la discusión de verificación vs búsqueda: para el problema de *contar* soluciones (no solo encontrar una), ¿crees que existe un algoritmo eficiente? ¿Por qué?
  No existe un algoritmo eficiente (de tiempo polinomial) conocido para el problema de contar todas las soluciones. 
Mientras que el problema de verificación es rápido y pertenece a la clase NP (toma un tiempo O(N^2) revisar un tablero lleno), y encontrar una sola solución también puede hacerse con atajos matemáticos, contar exige explorar de forma exhaustiva el árbol de decisiones para asegurar que no falte ninguna configuración válida. Este problema de conteo pertenece a la clase de complejidad #P-completo (Sharp-P completo), lo que significa que sufre de una explosión combinatoria ineludible a medida que crece N. 


---

## Cierre integrador

Responde las siguientes preguntas en el reporte. Cada respuesta debe ser argumentada con evidencia de los experimentos que realizaste.

1. Los cuatro problemas de esta práctica involucran explorar un espacio de soluciones. ¿Cuáles tienen estructura de **programación dinámica** (subproblemas que se repiten) y cuáles no? ¿Qué tienen en común los que sí la tienen?

2. El backtracking del laberinto y el de las N reinas son conceptualmente similares. ¿En qué se parecen su estructura recursiva? ¿En qué difieren el tipo de "poda" que realiza cada uno?

3. En la Parte 1 viste que la versión recursiva de Fibonacci era exponencial, pero después de agregar memoización bajó a O(n). ¿Podría aplicarse memoización al backtracking de las N reinas para mejorar su complejidad? Argumenta por qué sí o por qué no.

4. *(Pregunta abierta — sin respuesta única)* Si tuvieras que enseñar recursión a alguien que nunca la ha visto, ¿cuál de los cuatro problemas usarías como primer ejemplo? ¿Por qué?
