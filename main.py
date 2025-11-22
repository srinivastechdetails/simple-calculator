from fastapi import FastAPI, HTTPException
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from pydantic import BaseModel
import os

app = FastAPI()
app.add_middleware(GZipMiddleware, minimum_size=500)

# CORS middleware for development (allow all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple cache‑control middleware for static assets
class CacheControlMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        if request.url.path.startswith("/static"):
            response.headers["Cache-Control"] = "public, max-age=86400"
        return response

app.add_middleware(CacheControlMiddleware)

class CalculationRequest(BaseModel):
    a: float
    b: float

class CalculationResult(BaseModel):
    result: float

@app.post("/add", response_model=CalculationResult)
async def add(request: CalculationRequest):
    return {"result": request.a + request.b}

@app.post("/sub", response_model=CalculationResult)
async def sub(request: CalculationRequest):
    return {"result": request.a - request.b}

@app.post("/mul", response_model=CalculationResult)
async def mul(request: CalculationRequest):
    return {"result": request.a * request.b}

@app.post("/div", response_model=CalculationResult)
async def div(request: CalculationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": request.a / request.b}

# Health‑check endpoint
@app.get("/health")
async def health():
    return {"status": "ok"}

# Mount static files (HTML/JS/CSS)
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def read_index():
    return Response(open(os.path.join("static", "index.html")).read(), media_type="text/html")
