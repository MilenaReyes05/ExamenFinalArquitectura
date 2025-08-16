
from fastapi import FastAPI
from app.core.config import setup_cors
from app.api.v1 import router as api_v1

app = FastAPI(
    title="Microservicio de Optimización de Portafolio",
    version="1.0.0",
    description=(
        "Selecciona el conjunto óptimo de proyectos que maximiza la ganancia "
        "sin exceder la capacidad (presupuesto). Incluye documentación Swagger."
    ),
)

setup_cors(app)

@app.get("/", tags=["Sistema"], summary="Healthcheck")
def healthcheck():
    return {"status": "ok"}

app.include_router(api_v1)
