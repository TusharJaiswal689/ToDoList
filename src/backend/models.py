from database import Base
from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import validates

class Todos(Base):
    __tablename__= "todos"

    id= Column(Integer, primary_key= True, autoincrement=True, index=True)
    title= Column(String(50), nullable= False)
    description= Column(String(100))
    priority= Column(Integer, nullable= False)
    completed= Column(Boolean, default=False)

    __table_args__= (
        CheckConstraint("priority >= 1 AND priority <= 5", name= "check_priority_range"),
    )

    # ORM Level validation
    @validates("priority") #which column this decorator is validating.
    def validate_priority_range(self, key, value):
        if value is not None and not (1 <= value <=5):
            raise ValueError("priority must be between 1 and 5")
        return value