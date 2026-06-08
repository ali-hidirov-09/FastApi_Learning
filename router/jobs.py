from fastapi import APIRouter
from fastapi.params import Query
from pydantic import BaseModel, Field, SecretStr, EmailStr, ConfigDict
from typing import Optional
# from .users import User
from pydantic.alias_generators import to_camel

router = APIRouter()

class BaseSchema(BaseModel):
    # Mana bu konfiguratsiya hamma narsani hal qiladi!
    model_config = ConfigDict(
        alias_generator=to_camel, # snake_case -> camelCase
        populate_by_name=True,    # ham snake, ham camel'da qabul qilaveradi
        extra='forbid'            # begona narsaga "DAST" deydi
    )


@router.get("/name")
async def jobs_name():
    return {
        "job_count": 2,
        1: "Frontend",
        2: "Backend",
    }


class Job(BaseSchema):
    id: int = Field(gt=0)
    title: str
    description: str
    # author: User


@router.post("/create/{job_name}")
async def create_job(job:Job):
    return {"Muvaffaqiyatli yaratildi"}


@router.get("/jobs/")
async def read_jobs(
        category:str = Query("Backend", pattern="^Back$", alias="h!@#$%^&ufu", description='aaaaaaaaaaaa', title='aaaaaaaaaaaaaaaaaaaaaaaaaa'),
        limit: int=10
):
    return {
        "category":category,
        "limit":limit
    }


class Skill(BaseSchema):
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=3)


class Developer(BaseSchema):
    model_config = ConfigDict(extra='forbid')

    id: int = Field(..., gt=0)
    full_name: str = Field(..., min_length=3, max_length=20, description="Ismingizni kiriting")
    skills: list[Skill] = []


@router.post("/dev/create")
async def dev_create(developer: Developer):
    return {"message": " Muvaffaqiyatli yaratildi"}


class Freelancer(BaseSchema):
    email: EmailStr
    hourly_rate: float = Field(gt=10.0)
    api_key: SecretStr


freelancer = Freelancer(email="alihidiorh285@gmail.com", hourly_rate=25, api_key="super-secret-token-123")
print(freelancer.model_dump_json())
print(freelancer.api_key.get_secret_value())