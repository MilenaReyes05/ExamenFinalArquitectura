
from dataclasses import dataclass

@dataclass(frozen=True)
class Objeto:
    nombre: str
    peso: int
    ganancia: int
