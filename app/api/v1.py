
from fastapi import APIRouter, HTTPException
from app.schemas import SolicitudOptimizacion, Resultado
from app.models import Objeto
from app.services.optimizer import knapsack

router = APIRouter(tags=["Optimización"])

@router.post("/optimizar", response_model=Resultado, summary="Optimiza la selección de proyectos")
def optimizar(payload: SolicitudOptimizacion):
    # Validación adicional preventiva
    if payload.capacidad < 0:
        raise HTTPException(status_code=422, detail="capacidad debe ser >= 0")

    objetos = [Objeto(o.nombre, o.peso, o.ganancia) for o in payload.objetos]

    # Guardrail de tamaño para evitar cómputo excesivo n*W
    if len(objetos) * (payload.capacidad + 1) > 50_000_000:
        raise HTTPException(status_code=413, detail="Instancia demasiado grande para procesar")

    idx, ganancia_total, peso_total = knapsack(payload.capacidad, objetos)
    seleccionados = [objetos[i].nombre for i in idx]

    return Resultado(
        seleccionados=seleccionados,
        ganancia_total=ganancia_total,
        peso_total=peso_total
    )
