
from typing import List, Tuple
from app.models import Objeto

def _better(a: Tuple[int,int,int], b: Tuple[int,int,int]) -> bool:
    """
    Compara dos tuplas (ganancia, -peso, -count) y decide si 'a' es mejor que 'b'.
    Mayor ganancia es mejor. En empate, menor peso. Luego, menos elementos.
    """
    return a > b  # comparación lexicográfica

def knapsack(capacidad: int, objetos: List[Objeto]) -> Tuple[List[int], int, int]:
    """
    Resuelve 0/1 knapsack con programación dinámica.
    Retorna (indices_seleccionados, ganancia_total, peso_total).
    Desempates: misma ganancia -> menor peso -> menos elementos.
    """
    n = len(objetos)
    W = capacidad

    # dp[i][w] = tuple (ganancia, -peso, -count)
    dp = [ [(0, 0, 0) for _ in range(W + 1)] for _ in range(n + 1) ]
    keep = [ [False]*(W + 1) for _ in range(n + 1) ]

    for i in range(1, n+1):
        peso_i = objetos[i-1].peso
        gan_i = objetos[i-1].ganancia
        for w in range(W + 1):
            # Opción 1: no tomar i
            best = dp[i-1][w]

            # Opción 2: tomar i (si cabe)
            if peso_i <= w:
                prev = dp[i-1][w - peso_i]
                cand = (prev[0] + gan_i, prev[1] - peso_i, prev[2] - 1)
                if _better(cand, best):
                    best = cand
                    keep[i][w] = True

            dp[i][w] = best

    # Reconstrucción
    w = W
    idx = []
    for i in range(n, 0, -1):
        if keep[i][w]:
            idx.append(i-1)
            w -= objetos[i-1].peso

    idx.reverse()
    gan_total = sum(objetos[i].ganancia for i in idx)
    peso_total = sum(objetos[i].peso for i in idx)
    return idx, gan_total, peso_total
