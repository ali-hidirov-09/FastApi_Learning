from fastapi import APIRouter
from fastapi.params import Query
from pydantic import BaseModel, Field, SecretStr, EmailStr, ConfigDict, field_validator
from typing import Optional, Annotated
from .users import User
from pydantic.alias_generators import to_camel
from fastapi.responses import JSONResponse

router = APIRouter()

PositiveInt = Annotated[int, Field(gt=0)]
MinStr = Annotated[str, Field(min_length=3)]

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )







#---------------------------------------------------------Dars_5------------------------------------------------------------------


@router.post("/test-manual")
async def manual_response():
    return JSONResponse(
        status_code=418, # I'm a teapot (hazil status kodi)
        content={"message": "Men kofe damlay olmayman, men choynakman!"}
    )


class UserOut(BaseModel):
    username: str
    email: str


@router.post("/test-filter", response_model=UserOut,status_code=201)
async def test_filter(user:UserOut):
    # bu yerda aa ni kiritamiz lekin fast api uniauto qirqib tashlaydi
    raw_data = user.model_dump()
    raw_data["aaa"] = "aaaaa"
    print(raw_data)

    # Biz hammasini qaytaramiz (return raw_data)
    # Lekin response_model=UserOut bo'lgani uchun...
    return raw_data




#---------------------------------------------------------Dars_4------------------------------------------------------------------


class Job(BaseSchema):
    id: PositiveInt
    title: MinStr
    description: MinStr
    author: User


@router.post("/create/{job_name}")
async def create_job(job:Job):
    return {"Muvaffaqiyatli yaratildi"}


class Skill(BaseSchema):
    id: PositiveInt
    name: MinStr


class Developer(BaseSchema):

    id: PositiveInt
    full_name: MinStr = Field(..., max_length=20, description="Ismingizni kiriting")
    skills: list[Skill] = []
    
    @field_validator('full_name')
    @classmethod
    def name_must_be_alpha(cls, v:str):
        if not v.isalpha():
            raise ValueError("Ismda faqat xarflar bo'lisi shart")
        return v.title()


@router.post("/dev/create", response_model=Developer)
async def dev_create(developer: Developer):
    dev_data = developer.model_dump()

    return dev_data


class Freelancer(BaseSchema):
    email: EmailStr
    hourly_rate: float = Field(gt=10.0)
    api_key: SecretStr


freelancer = Freelancer(email="alihidiorh285@gmail.com", hourly_rate=25, api_key="super-secret-token-123")
print(freelancer.model_dump_json())
print(freelancer.api_key.get_secret_value())
#---------------------------------------------------------Dars_3------------------------------------------------------------------

@router.get("/jobs/")
async def read_jobs(
        category:str = Query("Backend", pattern="^Back$", alias="h!@#$%^&ufu", description='aaaaaaaaaaaa', title='aaaaaaaaaaaaaaaaaaaaaaaaaa'),
        limit: int=10
):
    return {
        "category":category,
        "limit":limit
    }



#---------------------------------------------------------Dars_2------------------------------------------------------------------
@router.get("/name")
async def jobs_name():
    return {
        "job_count": 2,
        1: "Frontend",
        2: "Backend",
    }
