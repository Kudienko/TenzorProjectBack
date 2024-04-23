from pydantic import BaseModel, EmailStr


class BaseUserCreate(BaseModel):
    login: str
    email: EmailStr
    hashed_password: str
    city: str | None = None


class BaseUserUpdate(BaseModel):
    login: str | None = None
    email: EmailStr | None = None
    hashed_password: str | None = None
    city: str | None = None


class UserRead(BaseModel):
    id: int
    email: EmailStr
    login: str
    city: str | None = None

    class Config:
        from_attributes = True


class UserCreate(BaseUserCreate):
    pass


class UserUpdate(BaseUserUpdate):
    pass
