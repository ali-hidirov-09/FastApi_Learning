from contextlib import asynccontextmanager
from fastapi import FastAPI
from router import api_router, NegativeSalaryError, my_handler
from fastapi.responses import RedirectResponse
from database import Base, engine
import models



@asynccontextmanager
async def lifespan(app: FastAPI):
    # Dastur ishga tushganda (startup) jadvallarni yaratadi
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title="ALI API",
    description="Junior python backend developerning ilk FAST API loyihasi",
    version="0.0.1",
    lifespan=lifespan
)

@app.get("/", include_in_schema=False)
async def redirect_to_docs():
    return RedirectResponse(url='/docs')

app.add_exception_handler(NegativeSalaryError, my_handler)
app.include_router(api_router, prefix="/api/v1")
