from fastapi import FastAPI
from router import api_router

app = FastAPI(
    title="ALI API",
    description="Junior python backend developerning ilk FAST API loyihasi",
    version="0.0.1"
)

app.include_router(api_router, prefix="/api/v1")


@app.options("/kopaytma/{son1}/{son2}", tags=["math"])
def kvadrat(son1:int, son2:int):
    s = son1*son2

    return {'Javob':f"{son1}*{son2}={s}"}


@app.get("/health", tags=["Health"])
def health():
    return {"status":"active", "DB": 'ok', "message":"Loyiha juda zo'r ishlab turibdi"}


@app.get("/info", tags=["Info"])
def info():
    return {
        "Version": "0.0.1",
        "engine": "uvicorn (ASGI)",
        "Framework": "Fast API",
        "Ega":"sceptik Ali va uning Phd ustozi Ai studio",
    }

@app.post("/items/{item_id}",tags=['items'])
def items(item_id:int):
    return {"Item":item_id}


