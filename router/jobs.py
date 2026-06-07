from fastapi import APIRouter

router = APIRouter()


@router.get("/name")
async def jobs_name():
    return {
        "job_count": 2,
        1: "Frontend",
        2: "Backend",
    }

@router.post("/create/{job_name}")
async def create_job(job_name):
    return {
        "id":2,
        "job_name": job_name,
        "message": "job muvaffaqiyart yaratildi"
    }