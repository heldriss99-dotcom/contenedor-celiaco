from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI(
    title="Sistema de Ubicaciones Sin Gluten - Guatemala",
    description="API para la gestion de establecimientos con opciones libres de gluten",
    version="1.0.0",
    docs_url=None,
    redoc_url=None
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Restaurant(BaseModel):
    name: str
    category: str
    description: str
    lat: float
    lng: float

def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "database"),
        database=os.getenv("DB_NAME", "celiaco"),
        user=os.getenv("DB_USER", "user"),
        password=os.getenv("DB_PASSWORD", "password"),
        port=os.getenv("DB_PORT", "5432")
    )

@app.get("/")
def inicio():
    return {"mensaje": "API activa"}

@app.get("/restaurants")
def obtener_restaurantes():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            description,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lng
        FROM restaurants
        ORDER BY id;
    """)

    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "lat": row[4],
            "lng": row[5]
        })

    cursor.close()
    conn.close()

    return data

@app.get("/restaurants/nearby")
def obtener_restaurantes_cercanos(
    lat: float = Query(...),
    lng: float = Query(...),
    radius_m: float = Query(...)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            category,
            description,
            ST_Y(location::geometry) AS lat,
            ST_X(location::geometry) AS lng,
            ST_Distance(
                location,
                ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography
            ) AS distance_m
        FROM restaurants
        WHERE ST_DWithin(
            location,
            ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography,
            %s
        )
        ORDER BY distance_m;
    """, (
        lng, lat,
        lng, lat, radius_m
    ))

    results = cursor.fetchall()

    data = []
    for row in results:
        data.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "description": row[3],
            "lat": row[4],
            "lng": row[5],
            "distance_m": row[6]
        })

    cursor.close()
    conn.close()

    return data

@app.post("/restaurants")
def crear_restaurante(restaurant: Restaurant):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO restaurants (name, category, description, location)
        VALUES (%s, %s, %s, ST_GeogFromText(%s))
    """, (
        restaurant.name,
        restaurant.category,
        restaurant.description,
        f"POINT({restaurant.lng} {restaurant.lat})"
    ))

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Registro agregado correctamente"}

@app.put("/restaurants/{restaurant_id}")
def actualizar_restaurante(restaurant_id: int, restaurant: Restaurant):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE restaurants
        SET
            name = %s,
            category = %s,
            description = %s,
            location = ST_GeogFromText(%s)
        WHERE id = %s
    """, (
        restaurant.name,
        restaurant.category,
        restaurant.description,
        f"POINT({restaurant.lng} {restaurant.lat})",
        restaurant_id
    ))

    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Registro actualizado correctamente"}

@app.delete("/restaurants/{restaurant_id}")
def eliminar_restaurante(restaurant_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM restaurants
        WHERE id = %s
    """, (restaurant_id,))

    if cursor.rowcount == 0:
        conn.rollback()
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="Registro no encontrado")

    conn.commit()
    cursor.close()
    conn.close()

    return {"mensaje": "Registro eliminado correctamente"}