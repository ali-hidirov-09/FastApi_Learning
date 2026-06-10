from fastapi import APIRouter
    from fastapi.params import Query
from pydantic import BaseModel, Field, SecretStr, EmailStr, ConfigDict, field_validator
from typing import Optional, Annotated
from .users import User
from pydantic.alias_generators import to_camel

router = APIRouter()

PositiveInt = Annotated[int, Field(gt=0)]
MinStr = Annotated[str, Field(min_length=3)]

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )


@router.get("/name")
async def jobs_name():
    return {
        "job_count": 2,
        1: "Frontend",
        2: "Backend",
    }


class Job(BaseSchema):
    id: PositiveInt
    title: MinStr
    description: MinStr
    author: User


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
    id: PositiveInt
    name: MinStr


class Developer(BaseSchema):
    model_config = ConfigDict(extra='forbid')

    id: PositiveInt
    full_name: MinStr = Field(..., max_length=20, description="Ismingizni kiriting")
    skills: list[Skill] = []
    
    @field_validator('full_name')
    @classmethod
    def name_must_be_alpha(cls, v:str):
        if not v.isalpha():
            return ValueError("Ismda faqat xarflar bo'lisi shart")
        return v.title()


@router.post("/dev/create")
async def dev_create(developer: Developer):
    return {"message": " Muvaffaqiyatli yaratildi",
            "Developer": developer
            }


class Freelancer(BaseSchema):
    email: EmailStr
    hourly_rate: float = Field(gt=10.0)
    api_key: SecretStr


freelancer = Freelancer(email="alihidiorh285@gmail.com", hourly_rate=25, api_key="super-secret-token-123")
print(freelancer.model_dump_json())
print(freelancer.api_key.get_secret_value())