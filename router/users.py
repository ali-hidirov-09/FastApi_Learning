from fastapi import APIRouter
from fastapi.params import Query, Path
from pydantic import BaseModel

router = APIRouter()

users_dict = {
        "user_1": {
            "id": 1,
            "Name": "Ali",
            "job": 'Backend developer', },

        "user_2": {
            "id": 2,
            "Name": "Vali",
            "job": 'Frontend developer'},

        "user_3": {
            "id": 3,
            "Name": "Mahmutali",
            "job": 'Devops developer'},

        "user_4": {
            "id": 4,
            "Name": "Botirali",
            "job": 'UX/UI developer'}
    }


@router.get("/all_users")
def get_all_users(
        q: str = Query(None, min_length=2, max_length=30)
):
    global users_dict
    return {
        "all_users":users_dict,
        "q":q
    }


@router.get("/{user_id}")
def get_user(
        user_id:int = Path(...,title="User id si", description="aniq kiriting", gt=0, le=100)

):
    global users_dict
    user = users_dict[f'user_{user_id}']
    return {
        "User": user
        }


class UserSchema(BaseModel):
    Name: str
    job: str


@router.post('/add_user')
def add_user(info:UserSchema):
    global users_dict
    last_id = int(list(users_dict.values())[-1]['id'])
    new_id = last_id + 1
    user_data = info.model_dump()
    user_data = {"id":new_id, **user_data}
    users_dict[f'user_{new_id}'] = user_data
    return {
        "info": user_data,
        "message": "User muvaffaqiyatli yaratildi"
    }