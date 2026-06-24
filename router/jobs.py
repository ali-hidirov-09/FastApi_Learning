from fastapi import APIRouter, Request, status, HTTPException
from fastapi.params import Query, Depends
from pydantic import BaseModel, Field, SecretStr, EmailStr, ConfigDict, field_validator, model_validator
from typing import Annotated
from .users import User
from pydantic.alias_generators import to_camel
from fastapi.responses import JSONResponse
from core.database import AsyncSession, get_async_session
from fastapi.security import OAuth2PasswordRequestForm
from core.security import create_access_token, hasher
router = APIRouter()

PositiveInt = Annotated[int, Field(gt=0)]
MinStr = Annotated[str, Field(min_length=3)]

class BaseSchema(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra='forbid'
    )


#---------------------------------------------------------Dars_13------------------------------------------------------------------

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db_user = {
        "username": "ali@gmail.com",
        "hashed_password": "$argon2id$v=19$m=65536,t=3,p=4$ilGq9d6b07r3/h/DWAsBQA$tht1dcFI8hh0FSNFDnUV42VLNgLj2jWkmLs8D/ci4+I"  # Bu 'password123' ning hashi
    }

    user_hashed_password = db_user['hashed_password']

    if not hasher.verify_password(form_data.password, user_hashed_password):
        raise HTTPException(401, detail="username yoki parol xato")

    return create_access_token(data={"sub": db_user['username']})







#---------------------------------------------------------Dars_9------------------------------------------------------------------
@router.get("/job_id")
async def read_job(db: AsyncSession = Depends(get_async_session)):
    print(db)
    return {"message": "muvaffaqiyatli ishladi"}



#---------------------------------------------------------Dars_7------------------------------------------------------------------
class NegativeSalaryError(Exception):
    def __init__(self, name:str):
        self.name = name


async def my_handler(request: Request, exc:NegativeSalaryError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"message": f"{exc.name}"}
    )

class Calculate(BaseSchema):
    salary: float


@router.post("/calculate-tax")
async def calculate(calculate: Calculate):
    data = calculate.model_dump()
    if data['salary'] < 500:
        raise NegativeSalaryError(name="Maosh manfiy bo'lishi mumkin emas, bu qullik davri emas!")
    return data


#---------------------------------------------------------Dars_6------------------------------------------------------------------



password = Annotated[str, Field(min_length=8, max_length=50)]

class Account(BaseSchema):
    password: password
    confirm_password: password
    salary_min: float = Field(ge=500)
    salary_max: float = Field(ge=500.0)

    @model_validator(mode='after')
    def check_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError("Parollar bir biriga mos kelamydi")
        return self


    @model_validator(mode='after')
    def check_salaries(self):
        if self.salary_min > self.salary_max:
            raise ValueError("salary_min salary_max dan katta bo'lishi mumkin emas")
        return self


MinStr = Annotated[str, Field(min_length=3)]
phoneNuber = Annotated[str, Field(pattern=r"^\+998\d{9}$")]
aaa = Annotated[str, Field(pattern=r"^admin-\d{2}-\w{5}-\s+$")]
class User1(BaseSchema):
    username: MinStr
    phone_number: phoneNuber
    a: aaa

@router.post("/get_post", response_model=User1)
async def post_get(user:User1):
    user_data = user.model_dump()
    return user_data

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
