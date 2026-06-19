from fastapi import FastAPI
from router import api_router, NegativeSalaryError, my_handler
from fastapi.responses import RedirectResponse
from database import Base, engine
import models

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = FastAPI(
    title="ALI API",
    description="Junior python backend developerning ilk FAST API loyihasi",
    version="0.0.1"
)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url='/docs')

app.add_exception_handler(NegativeSalaryError, my_handler)
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


