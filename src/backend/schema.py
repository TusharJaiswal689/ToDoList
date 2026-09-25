from pydantic import BaseModel, EmailStr, Field, ConfigDict

# -----CREATE-----
class UserCreate(BaseModel):

    email: EmailStr= Field(...)
    username: str= Field(..., min_length=3)
    first_name: str= Field(..., min_length=3)
    last_name: str= Field(..., min_length=3)
    hashed_password: str= Field(..., min_length=12)

class TodoCreate(BaseModel):

    title: str = Field(..., max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = Field(False)
    owner: int = Field(...,gt=0)

#-----RESPONSE-----
class UserResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str | None = None

class TodoResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool
    owner: int

#-----UPDATE-----

class UserUpdate(BaseModel):

    email: EmailStr | None = Field(None)
    username: str | None= Field(None, min_length=3)
    first_name: str | None= Field(None, min_length=3)
    last_name: str | None= Field(None, min_length=3)
    hashed_password: str | None= Field(None, min_length=12)

class TodoUpdate(BaseModel):

    title: str | None = Field(None, max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int | None = Field(None, ge=1, le=5)
    completed: bool | None = Field(None)
    owner: int | None = Field(None,gt=0)