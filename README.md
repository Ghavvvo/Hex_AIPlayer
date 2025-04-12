# Informe del Proyecto de IA para Hex

## Estructura del Proyecto
El proyecto está organizado en dos archivos principales:

- **player.py**: Contiene la implementación del jugador.
- **utils.py**: Funciones auxiliares para manipular el tablero.

## Estructura del Código
La clase `IAPlayer` hereda de `Player` e implementa:
- Inicialización con IDs de jugador y oponente
- Método `play()` que decide el movimiento
- Funciones internas para evaluación heurística y búsqueda minimax

El archivo `utils.py` proporciona funciones básicas para:
- Eliminar fichas del tablero (`remove_piece`)
- Verificar posiciones válidas (`is_on_board`)
## Jugadas Iniciales Predefinidas
La IA implementa una estrategia de apertura:

- **Primer movimiento**: Siempre intenta ocupar la casilla central del tablero si está disponible.
- **Respuesta a apertura central**: Si el oponente ha ocupado el centro, la IA juega en la casilla adyacente izquierda al centro (middle, middle-1).

Esta estrategia aprovecha la importancia estratégica de dominar el centro en Hex, donde controlar esta posición proporciona mayor flexibilidad para conectar ambos lados del tablero.

## Algoritmo Minimax
El algoritmo minimax explora sistemáticamente el árbol de posibles movimientos, alternando entre la maximización de nuestras oportunidades y la minimización de las del oponente. La poda alfa-beta optimiza este proceso eliminando ramas que no afectarán el resultado final.

## Heurística
La función de evaluación `evaluate()` combina varios aspectos del juego:

### Heurística Base:
- Evalúa cada fila (para el jugador 1) o columna (para el jugador 2).
- Asigna 5 puntos por cada ficha propia en la línea.
- Bonus de 2 puntos por cada ficha propia adyacente en diagonal ([-1,1] y [1,-1]).
- Representa la forma direccional del juego, donde las fichas en la misma fila/columna son más valiosas.

### Conteo de Componentes:
- Cuenta componentes conexas de fichas para ambos jugadores.
- Usa un sistema de búsqueda en profundidad (DFS) para identificar componentes conectados.
- Resta los componentes del oponente a los propios y multiplica por 2.
- Premia la IA por tener más componentes conectados, lo que indica una mejor posición en el tablero.

La heurística final combina estos aspectos: `base_heuristic() + (own_components - opp_components) * 2`.
Esto combina la evaluación de la posición actual con el conteo de componentes, proporcionando una medida más completa de la situación en el tablero.

## Manejo de Profundidad
La IA ajusta dinámicamente la profundidad de búsqueda según la cantidad de movimientos disponibles:

- **Más de 20 movimientos posibles**: Profundidad 3 (fase inicial del juego).
- **Entre 10 y 20 movimientos**: Profundidad 6 (fase media).
- **Menos de 10 movimientos**: Profundidad 8 (final del juego).

Esto optimiza el tiempo de búsqueda, dedicando más recursos a posiciones críticas donde hay menos opciones disponibles.

## Optimizaciones
- **Poda Alfa-Beta**: Implementada en el algoritmo minimax para reducir el espacio de búsqueda.
- **Evaluación Temprana**: Verifica condiciones de victoria antes de evaluar la heurística.
- **Bonus por Profundidad**: Ajusta los valores de victoria/derrota según la profundidad (+1000 + depth para victoria, -1000 - depth para derrota), priorizando victorias más rápidas y retrasando posibles derrotas.

