# Microservicio de Optimización de Portafolio - FastAPI

Servicio en **Python + FastAPI** con documentación **Swagger/OpenAPI**, que expone el endpoint `POST /optimizar` para seleccionar el conjunto óptimo de proyectos que maximiza la ganancia sin exceder la **capacidad** (presupuesto).

## 🚀 Requisitos
- Python 3.11+
- `pip`

## 📦 Instalación (local)
```bash
# 1) Crear y activar entorno virtual (opcional)
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate

# 2) Instalar dependencias
pip install -r requirements.txt
```

## ▶️ Ejecución (local)
```bash
uvicorn app.main:app --reload
```
- Swagger UI: http://127.0.0.1:8000/docs  
- OpenAPI JSON: http://127.0.0.1:8000/openapi.json
- ReDoc: http://127.0.0.1:8000/redoc
- frontend: entrar a la ruta /frontend_optimizador y abrir el archivo index.html

## 🧪 Pruebas
```bash
pip install -r requirements-dev.txt
pytest -q
```

## 🐳 Docker
```bash
# Construir imagen
docker build -t portafolio-api:latest .
# Ejecutar
docker run --rm -p 8000:8000 portafolio-api:latest
```

## ✉️ Ejemplo de petición
```bash
curl -X POST "http://127.0.0.1:8000/optimizar"   -H "Content-Type: application/json"   -d '{
    "capacidad": 10000,
    "objetos": [
      {"nombre": "A", "peso": 2000, "ganancia": 1500},
      {"nombre": "B", "peso": 4000, "ganancia": 3500},
      {"nombre": "C", "peso": 5000, "ganancia": 4000},
      {"nombre": "D", "peso": 3000, "ganancia": 2500}
    ]
  }'
```

Respuesta:
```json
{
  "seleccionados": ["B", "C"],
  "ganancia_total": 7500,
  "peso_total": 9000
}
```

> **Notas:** El modelo y los ejemplos siguen el enunciado del examen. La API valida entradas y maneja casos límite (capacidad=0, pesos=0, nombres duplicados, etc.).

## 🧠 Algoritmo
Se implementa **programación dinámica (0/1 knapsack)** con reconstrucción del conjunto óptimo y reglas de desempate **(misma ganancia ⇒ menor peso ⇒ menos elementos ⇒ orden estable)** para resultados deterministas.

## 📁 Estructura
```
optimizador_portafolio/
├─ app/
│  ├─ api/
│  │  └─ v1.py
│  ├─ core/
│  │  └─ config.py
│  ├─ services/
│  │  └─ optimizer.py
│  ├─ schemas.py
│  ├─ models.py
│  └─ main.py
├─ frontend_optimizador/
├─ tests/
│  ├─ test_api.py
│  └─ test_service.py
├─ requirements.txt
├─ requirements-dev.txt
├─ Dockerfile
└─ README.md
```

## 📜 Licencia
Milena Reyes