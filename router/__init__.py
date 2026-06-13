from router import jobs,users
from fastapi import APIRouter
from .jobs import my_handler, NegativeSalaryError
api_router = APIRouter()


api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
