
import pytest
from app.models import Objeto
from app.services.optimizer import knapsack

def test_knapsack_basico():
    objs = [
        Objeto("A", 2, 3),
        Objeto("B", 3, 4),
        Objeto("C", 4, 5),
        Objeto("D", 5, 8),
    ]
    idx, gan, peso = knapsack(5, objs)
    # Óptimo: D (5,8)
    assert gan == 8
    assert peso == 5
    assert [objs[i].nombre for i in idx] == ["D"]

def test_knapsack_cero_capacidad():
    objs = [Objeto("X", 10, 100)]
    idx, gan, peso = knapsack(0, objs)
    assert gan == 0 and peso == 0 and idx == []

def test_knapsack_pesos_cero():
    # Todos caben, ganancia suma total
    objs = [
        Objeto("x1", 0, 5),
        Objeto("x2", 0, 7),
        Objeto("y", 3, 10),
    ]
    idx, gan, peso = knapsack(1, objs)
    assert gan in (12, 12 + 0, 12)  # 5 + 7, más posibles de peso 0
    assert peso == 0 or peso == 0  # los de peso 0 no consumen capacidad
    # Debe incluir x1 y x2 (peso 0) como mínimo
    sel = [objs[i].nombre for i in idx]
    assert "x1" in sel and "x2" in sel

def test_knapsack_duplicados():
    objs = [
        Objeto("A", 4, 5),
        Objeto("A", 4, 5),
        Objeto("B", 2, 3),
    ]
    idx, gan, peso = knapsack(6, objs)
    # Óptimo: A (4,5) + B (2,3) = (6,8)
    assert gan == 8 and peso == 6
