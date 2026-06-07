from fastapi import APIRouter
from fastapi.params import Query
from pydantic.v1.validators import pattern_validator

router = APIRouter()


@router.get("/name")
async def jobs_name():
    return {
        "job_count": 2,
        1: "Frontend",
        2: "Backend",
    }

@router.post("/create/{job_name}")
async def create_job(job_name:str="ALI"):
    return {
        "id":2,
        "job_name": job_name,
        "message": "job muvaffaqiyart yaratildi"
    }


@router.get("/jobs/")
async def read_jobs(
        category:str = Query("Backend", pattern="^Back$", alias="h!@#$%^&ufu", description='aaaaaaaaaaaa', title='aaaaaaaaaaaaaaaaaaaaaaaaaa'),
        limit: int=10
):
    return {
        "category":category,
        "limit":limit
    }