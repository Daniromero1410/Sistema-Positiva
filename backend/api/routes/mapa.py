from fastapi import APIRouter, Query
from typing import Optional

router = APIRouter()

# Coordenadas de ciudades principales de Colombia
COORDENADAS = {
    "BOGOTA": {"lat": 4.7110, "lon": -74.0721},
    "MEDELLIN": {"lat": 6.2476, "lon": -75.5658},
    "CALI": {"lat": 3.4516, "lon": -76.5320},
    "BARRANQUILLA": {"lat": 10.9685, "lon": -74.7813},
    "BUCARAMANGA": {"lat": 7.1193, "lon": -73.1227},
    "CARTAGENA": {"lat": 10.3997, "lon": -75.5144},
    "CUCUTA": {"lat": 7.8939, "lon": -72.5078},
    "PEREIRA": {"lat": 4.8087, "lon": -75.6906},
    "IBAGUE": {"lat": 4.4389, "lon": -75.2322},
    "PASTO": {"lat": 1.2136, "lon": -77.2811},
    "MANIZALES": {"lat": 5.0703, "lon": -75.5138},
    "VILLAVICENCIO": {"lat": 4.1420, "lon": -73.6266},
    "VALLEDUPAR": {"lat": 10.4631, "lon": -73.2532},
    "NEIVA": {"lat": 2.9273, "lon": -75.2819},
    "SANTA MARTA": {"lat": 11.2408, "lon": -74.1990},
}

@router.get("/datos")
async def get_datos_mapa(
    ano: Optional[int] = None,
    departamento: Optional[str] = None
):
    """Obtiene datos para visualizar en el mapa."""

    # Datos de ejemplo basados en la maestra real
    datos = [
        {"ciudad": "BOGOTA", "departamento": "BOGOTA", "contratos": 135, "alertas": 5},
        {"ciudad": "MEDELLIN", "departamento": "ANTIOQUIA", "contratos": 29, "alertas": 2},
        {"ciudad": "BUCARAMANGA", "departamento": "SANTANDER", "contratos": 24, "alertas": 1},
        {"ciudad": "BARRANQUILLA", "departamento": "ATLANTICO", "contratos": 32, "alertas": 3},
        {"ciudad": "CALI", "departamento": "VALLE DEL CAUCA", "contratos": 28, "alertas": 2},
        {"ciudad": "CARTAGENA", "departamento": "BOLIVAR", "contratos": 23, "alertas": 1},
        {"ciudad": "CUCUTA", "departamento": "NORTE DE SANTANDER", "contratos": 18, "alertas": 0},
        {"ciudad": "PEREIRA", "departamento": "RISARALDA", "contratos": 19, "alertas": 1},
        {"ciudad": "IBAGUE", "departamento": "TOLIMA", "contratos": 19, "alertas": 0},
        {"ciudad": "PASTO", "departamento": "NARIÑO", "contratos": 20, "alertas": 2},
    ]

    # Agregar coordenadas
    for item in datos:
        coords = COORDENADAS.get(item["ciudad"], {})
        item["lat"] = coords.get("lat", 4.5)
        item["lon"] = coords.get("lon", -74.0)

    # Aplicar filtros
    if departamento:
        datos = [d for d in datos if d["departamento"] == departamento]

    return {
        "total_contratos": sum(d["contratos"] for d in datos),
        "ciudades_unicas": len(datos),
        "datos": datos,
        "centro": {"lat": 4.5709, "lon": -74.2973},  # Centro de Colombia
        "zoom": 5
    }

@router.get("/top-ciudades")
async def get_top_ciudades(limit: int = 10):
    """Top ciudades por cantidad de contratos."""

    return [
        {"posicion": 1, "ciudad": "BOGOTA", "departamento": "BOGOTA", "contratos": 135},
        {"posicion": 2, "ciudad": "BARRANQUILLA", "departamento": "ATLANTICO", "contratos": 32},
        {"posicion": 3, "ciudad": "MEDELLIN", "departamento": "ANTIOQUIA", "contratos": 29},
        {"posicion": 4, "ciudad": "CALI", "departamento": "VALLE DEL CAUCA", "contratos": 28},
        {"posicion": 5, "ciudad": "BUCARAMANGA", "departamento": "SANTANDER", "contratos": 24},
        {"posicion": 6, "ciudad": "CARTAGENA", "departamento": "BOLIVAR", "contratos": 23},
        {"posicion": 7, "ciudad": "PASTO", "departamento": "NARIÑO", "contratos": 20},
        {"posicion": 8, "ciudad": "PEREIRA", "departamento": "RISARALDA", "contratos": 19},
        {"posicion": 9, "ciudad": "IBAGUE", "departamento": "TOLIMA", "contratos": 19},
        {"posicion": 10, "ciudad": "CUCUTA", "departamento": "N. SANTANDER", "contratos": 18},
    ][:limit]

@router.get("/departamentos")
async def get_contratos_por_departamento():
    """Contratos agrupados por departamento."""

    return [
        {"departamento": "BOGOTA", "contratos": 135, "porcentaje": 14.6},
        {"departamento": "ANTIOQUIA", "contratos": 61, "porcentaje": 6.6},
        {"departamento": "SANTANDER", "contratos": 46, "porcentaje": 5.0},
        {"departamento": "ATLANTICO", "contratos": 40, "porcentaje": 4.3},
        {"departamento": "VALLE DEL CAUCA", "contratos": 36, "porcentaje": 3.9},
        {"departamento": "NARIÑO", "contratos": 36, "porcentaje": 3.9},
        {"departamento": "TOLIMA", "contratos": 31, "porcentaje": 3.4},
        {"departamento": "CESAR", "contratos": 30, "porcentaje": 3.2},
        {"departamento": "META", "contratos": 30, "porcentaje": 3.2},
        {"departamento": "OTROS", "contratos": 480, "porcentaje": 51.9},
    ]
