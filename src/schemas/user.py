from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    name: str = Field(None, title="User name", max_length=512)
    skills: str = Field(None, title="Skills", max_length=2048)
    email: EmailStr = Field(title="Email address")


class UserRegister(UserBase):
    password: str = Field(title="Password")


class UserDelete(BaseModel):
    password: str = Field(title="Password")


class UserUpdateData(BaseModel):
    name: str = Field(title="User name")
    old_password: str = Field(title="Old password")
    new_password: str = Field(title="New password")