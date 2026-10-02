# el que define el router con los endpoints

from fastapi import APIRouter, HTTPException, status
from models.users import (
    UpdateUserResponse,
    User,
    GetUsersResponse,
    CreateUserResponse,
    DeleteUserResponse,
)

router = APIRouter()

usuarios: list[User] = [
    User(id=1, name="juan perez"),
    User(id=2, name="pepe sanchez"),
]

# Lista todos los usuarios
@router.get("/user") 
def get_users(is_active: bool | None = None) -> GetUsersResponse:
    r = GetUsersResponse(users=[user for user in usuarios if user.is_active == is_active])
    return r

# Elimina un usuario por id
@router.delete("/user/{id}")
def delete_user(id: int) -> DeleteUserResponse:
    for user in usuarios:
        if user.id == id:
            usuarios.remove(user)
            return DeleteUserResponse(message="usuario borrado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )

# Crea un usuario
@router.post("/user")
def create_user(user: User) -> CreateUserResponse:
    usuarios.append(user)
    return CreateUserResponse(message="usuario creado")

# Actualiza un usuario por id
@router.put("/user/{id}")
def update_user(id: int, user: User) -> UpdateUserResponse:
    for i, u in enumerate(usuarios):
        if u.id == id:
            usuarios[i] = user
            return UpdateUserResponse(message="usuario actualizado")

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Usuario no encontrado"
    )