from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from fastapi.responses import FileResponse
import os

app = FastAPI()

class CalculationRequest(BaseModel):
    a: float
    b: float

@app.post("/add")
async def add(request: CalculationRequest):
    return {"result": request.a + request.b}

@app.post("/sub")
async def sub(request: CalculationRequest):
    return {"result": request.a - request.b}

@app.post("/mul")
async def mul(request: CalculationRequest):
    return {"result": request.a * request.b}

@app.post("/div")
async def div(request: CalculationRequest):
    if request.b == 0:
        raise HTTPException(status_code=400, detail="Division by zero")
    return {"result": request.a / request.b}

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('static/index.html')
