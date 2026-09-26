from pydantic import BaseModel, EmailStr, Field, ConfigDict

# -----USERS-----
class UserCreate(BaseModel):

    email: EmailStr= Field(..., unique=True)
    username: str= Field(..., min_length=3)
    first_name: str= Field(..., min_length=3)
    last_name: str= Field(..., min_length=3)
    password: str= Field(..., min_length=12)

class UserResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    hashed_password: str | None = None

class UserUpdate(BaseModel):

    email: EmailStr | None = Field(None)
    username: str | None= Field(None, min_length=3)
    first_name: str | None= Field(None, min_length=3)
    last_name: str | None= Field(None, min_length=3)

class UserPassUpdate(BaseModel):
    password: str = Field(...,min_length=12)

#-----TODOS-----

class TodoCreate(BaseModel):

    title: str = Field(..., max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = Field(False)

class TodoResponse(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool
    owner: int

class TodoUpdate(BaseModel):

    title: str | None = Field(None, max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int | None = Field(None, ge=1, le=5)
    completed: bool | None = Field(None)


#-----AUTHENTICATION-----

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., min_length=3)
    password: str = Field(..., min_length=12)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"