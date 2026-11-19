import random

from fastapi import FastAPI, HTTPException, Query

app = FastAPI(title="Number / Random / Fact API", version="1.0.0")

FACTS = [
    "Осьминоги имеют три сердца.",
    "Мёд никогда не портится.",
    "Свет от Солнца до Земли идёт около 8 минут.",
    "У уток водонепроницаемое оперение.",
    "Банан — это ягода, а клубника — нет.",
    "Человеческий мозг на ~73% состоит из воды.",
    "Гром в 5 раз горячее поверхности Солнца.",
    "Пауки могут жить без еды до года.",
]


@app.get("/")
async def root():
    return {
        "message": "Welcome to the Number/Random/Fact API",
        "endpoints": ["/health", "/api/random", "/api/fact", "/api/dice"],
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/api/random")
async def random_number(
    min: int = Query(1, ge=-1_000_000, le=1_000_000),
    max: int = Query(100, ge=-1_000_000, le=1_000_000),
):
    if min > max:
        raise HTTPException(status_code=400, detail="min не может быть больше max")
    return {"min": min, "max": max, "random": random.randint(min, max)}


@app.get("/api/fact")
async def fact():
    return {"fact": random.choice(FACTS)}


@app.get("/api/dice")
async def dice(
    sides: int = Query(6, ge=2, le=100, description="Количество граней кубика"),
    count: int = Query(1, ge=1, le=20, description="Количество бросков"),
):
    rolls = [random.randint(1, sides) for _ in range(count)]
    return {"sides": sides, "count": count, "rolls": rolls, "sum": sum(rolls)}
