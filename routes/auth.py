from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database.database import async_session
from models.user import User
from sqlmodel import select
from passlib.context import CryptContext
from schemas.user import UserCreate, UserLogin, UserUpdateUsername, UserUpdateEmail, UserUpdatePassword

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Dependency pentru sesiune DB
async def get_session():
    async with async_session() as session:
        yield session

@router.post("/register")
async def register(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password
    )

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return {"message": "User registered", "user_id": user.id}

@router.post("/login")
async def login(login_data: UserLogin, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.email == login_data.email))
    user = result.scalar_one_or_none()

    if not user or not pwd_context.verify(login_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful", "user_id": user.id}

@router.get("/user/{user_id}")
async def get_user_info(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }

@router.put("/user/{user_id}/update/username")
async def update_username(user_id: int, data: UserUpdateUsername, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = data.username
    session.add(user)
    await session.commit()
    return {"message": "Username updated"}

@router.put("/user/{user_id}/update/email")
async def update_email(user_id: int, data: UserUpdateEmail, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.email = data.email
    session.add(user)
    await session.commit()
    return {"message": "Email updated"}

@router.put("/user/{user_id}/update/password")
async def update_password(user_id: int, data: UserUpdatePassword, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password_hash = pwd_context.hash(data.password)
    session.add(user)
    await session.commit()
    return {"message": "Password changed"}

@router.delete("/user/{user_id}/delete")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user)
    await session.commit()
    return {"message": "User deleted"}
