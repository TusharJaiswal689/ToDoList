from pydantic import BaseModel, Field, ConfigDict

class TodoCreate(BaseModel):
    model_config = ConfigDict(from_attributes= True)

    title: str = Field(..., max_length=50, )
    description: str | None = Field(None, max_length=100)
    priority: int = Field(..., ge=1, le=5)
    completed: bool = Field(False)

class TodoOut(BaseModel):
    model_config= ConfigDict(from_attributes=True)
    
    id: int
    title: str
    description: str | None = None
    priority: int
    completed: bool