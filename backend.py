# backend.py
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import random

app = FastAPI()

# CORS 設定（フロント用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 実運用はフロントのURLに限定
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# キャッシュ用（例: 1秒以内のアクセスは同じ値を返す）
_last_cache = None
_last_time = 0
CACHE_TTL = 1  # 秒

async def generate_data():
    # ドーナツチャート用
    total_ai = 50
    normal = random.randint(30, 45)
    evolve = total_ai - normal

    # バーチャート用（例: 月～金）
    bar_chart = {
        "月": random.randint(150, 200),
        "火": random.randint(100, 180),
        "水": random.randint(130, 210),
        "木": random.randint(120, 180),
        "金": random.randint(100, 150)
    }

    data = {
        "donut": {
            "totalAI": total_ai,
            "normal": normal,
            "evolve": evolve
        },
        "stats": {
            "activeAI": 47,
            "completedTasks": 1284,
            "averagePerformance": 96.4,
            "ongoingEvolution": 12
        },
        "barChart": bar_chart
    }
    return data

@app.get("/data", response_class=ORJSONResponse)
async def get_dashboard_data():
    global _last_cache, _last_time
    now = asyncio.get_event_loop().time()
    if _last_cache and now - _last_time < CACHE_TTL:
        return _last_cache
    data = await generate_data()
    _last_cache = data
    _last_time = now
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend:app", host="0.0.0.0", port=8000, reload=True)
