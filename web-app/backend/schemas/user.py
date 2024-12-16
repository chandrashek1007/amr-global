from pydantic import BaseModel, EmailStr, constr

# Base schema for shared fields
class UserBase(BaseModel):
    name: constr(max_length=50)  # Limit the length of the name to 50 characters
    email: EmailStr  # Validate email format

# Schema for creating a new user
class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128)  # Enforce password length constraints
    phone_no: constr(max_length=15)  # Optional, but with a max length

# Schema for returning user details
class UserResponse(UserBase):
    id: int
    phone_no: str

    class Config:
        orm_mode = True
