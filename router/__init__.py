from router import jobs,users, auth
from fastapi import APIRouter
from .jobs import my_handler, NegativeSalaryError
api_router = APIRouter()


api_router.include_router(jobs.router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(users.router, prefix="/users", tags=['Users'])
api_router.include_router(auth.router, prefix="/auth", tags=['Auth'])
