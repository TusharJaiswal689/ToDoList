from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserCreate(BaseModel):
    model_config= ConfigDict(from_attributes=True)

    email: EmailStr= Field(...)
    username: str= Field(..., min_length=3)
    first_name: str= Field(..., min_length=3)
    last_name: str= Field(..., min_length=3)
    password: str= Field(..., min_length=12)

class TodoCreate(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    title: str = Field(..., max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = Field(False)
    owner: int = Field(...,gt=0)

class UserResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    password: str | None = None

class TodoResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool