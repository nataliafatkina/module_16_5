from fastapi import FastAPI, Path, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI(swagger_ui_parameters={"tryItOutEnabled": True}, debug=True)

# Настраиваем Jinja2 для загрузки шаблонов из папки templates
templates = Jinja2Templates(directory="templates")

users = []

class User(BaseModel):
        id: int
        username: str
        age: int

@app.get('/')
async def get_all_users(request: Request) -> HTMLResponse:
    return templates.TemplateResponse('users.html', {'request': request, 'users': users})

@app.get('/user/{user_id}')
async def get_user(request: Request, user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> HTMLResponse:
    for user in users:
        if user.id == user_id:
            return templates.TemplateResponse('users.html', {'request': request, 'user': user})
    else:
        raise HTTPException(status_code=404, detail='User was not found')

@app.post('/user/{username}/{age}')
async def add_user(username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                   age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    user_id = max((user.id for user in users), default=0) + 1
    new_user = User(id=user_id, username=username, age=age)
    users.append(new_user)
    return new_user

@app.put('/user/{user_id}/{username}/{age}')
async def update_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')],
                      username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='UrbanUser')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='24')]) -> User:
    for user in users:
        if user.id == user_id:
            user.username = username
            user.age = age
            return user
    else:
        raise HTTPException(status_code=404, detail='User was not found')

@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(ge=1, le=100, description='Enter User ID', example='1')]) -> User:
    for i, user in enumerate(users):
        if user.id == user_id:
            user_deleted = users.pop(i)
            return user_deleted
    else:
        raise HTTPException(status_code=404, detail='User was not found')

