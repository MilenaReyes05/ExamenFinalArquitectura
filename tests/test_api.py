
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_optimizar_happy_path():
    payload = {
        "capacidad": 10000,
        "objetos": [
            {"nombre": "A", "peso": 2000, "ganancia": 1500},
            {"nombre": "B", "peso": 4000, "ganancia": 3500},
            {"nombre": "C", "peso": 5000, "ganancia": 4000},
            {"nombre": "D", "peso": 3000, "ganancia": 2500},
            {"nombre": "E", "peso": 1500, "ganancia": 1800}
        ]
    }
    r = client.post("/optimizar", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "ganancia_total" in data
    assert "peso_total" in data
    assert data["peso_total"] <= payload["capacidad"]

def test_validacion():
    bad = {"capacidad": -1, "objetos":[{"nombre":"x","peso":1,"ganancia":1}]}
    r = client.post("/optimizar", json=bad)
    assert r.status_code in (422, 400)

def test_instancia_demasiado_grande():
    # n*W > 50M para gatillar el guardrail sin consumir RAM
    W = 5_000_001
    payload = {"capacidad": W, "objetos":[{"nombre":"x","peso":0,"ganancia":0}]}
    r = client.post("/optimizar", json=payload)
    assert r.status_code == 413
