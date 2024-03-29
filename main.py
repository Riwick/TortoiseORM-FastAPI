from typing import List

from fastapi import FastAPI
from starlette.exceptions import HTTPException
from pydantic import BaseModel
from tortoise.contrib.fastapi import register_tortoise

from models import User_Pydantic, Users, UserIn_Pydantic

app = FastAPI(title='TortoiseORM+FastAPI', openapi_url='/api/v1/openapi.json')


class Status(BaseModel):
    message: str


@app.get('/users', response_model=List[User_Pydantic])
async def get_users():
    return await User_Pydantic.from_queryset(Users.all())


@app.post("/users", response_model=User_Pydantic)
async def create_user(user: UserIn_Pydantic):
    user_obj = await Users.create(**user.model_dump(exclude_unset=True))
    return await User_Pydantic.from_tortoise_orm(user_obj)


@app.get("/users/{user_id}", response_model=User_Pydantic)
async def get_user(user_id: int):
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.put('/users/{user_id}', response_model=User_Pydantic)
async def update_user(user_id: int, user: UserIn_Pydantic):
    await Users.filter(id=user_id).update(**user.model_dump(exclude_unset=True))
    return await User_Pydantic.from_queryset_single(Users.get(id=user_id))


@app.delete('/users/{user_id}', response_model=Status)
async def delete_user(user_id: int):
    deleted_count = await Users.filter(id=user_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f'User {user_id} not found')
    return Status(message=f'Deleted user {user_id}')


register_tortoise(
    app,
    config={
            'connections': {
                'default': {
                    'engine': 'tortoise.backends.asyncpg',
                    'credentials': {
                        'host': 'localhost',
                        'port': '10000',
                        'user': 'postgres',
                        'password': 'postgres',
                        'database': 'postgres',
                    }
                },
                'default': 'postgres://postgres:postgres@localhost:10000/postgres'
            },
            'apps': {
                'models': {
                    'models': ['models'],
                    'default_connection': 'default',
                }
            }
    },
    generate_schemas=True,
    add_exception_handlers=True
)
