
from typing import List
from pydantic import BaseModel, Field

class ObjetoIn(BaseModel):
    nombre: str = Field(..., min_length=1, description="Nombre del proyecto/inversión")
    peso: int = Field(..., ge=0, description="Costo requerido (entero, >=0)")
    ganancia: int = Field(..., ge=0, description="Beneficio esperado (entero, >=0)")

    class Config:
        json_schema_extra = {
            "example": {"nombre": "A", "peso": 2000, "ganancia": 1500}
        }

class SolicitudOptimizacion(BaseModel):
    capacidad: int = Field(..., ge=0, description="Límite presupuestario (>=0)")
    objetos: List[ObjetoIn] = Field(..., min_items=0)

    class Config:
        json_schema_extra = {
            "example": {
                "capacidad": 10000,
                "objetos": [
                    {"nombre": "A", "peso": 2000, "ganancia": 1500},
                    {"nombre": "B", "peso": 4000, "ganancia": 3500},
                    {"nombre": "C", "peso": 5000, "ganancia": 4000},
                    {"nombre": "D", "peso": 3000, "ganancia": 2500}
                ]
            }
        }

class Resultado(BaseModel):
    seleccionados: List[str]
    ganancia_total: int
    peso_total: int

    class Config:
        json_schema_extra = {
            "example": {
                "seleccionados": ["B", "C"],
                "ganancia_total": 7500,
                "peso_total": 9000
            }
        }
