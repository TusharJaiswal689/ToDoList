from typing import List

from sqlalchemy import ForeignKey, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, validates, relationship
from database.db_config import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int]= mapped_column(Integer, primary_key=True, autoincrement=True, index= True)
    email: Mapped[str]= mapped_column(String, nullable=False, unique= True)
    username: Mapped[str]= mapped_column(String, nullable=False, unique=True)
    first_name: Mapped[str]= mapped_column(String, nullable=False)
    last_name: Mapped[str]= mapped_column(String, nullable=False)
    hashed_password: Mapped[str]= mapped_column(String, nullable=False)
    is_active: Mapped[bool]= mapped_column(Boolean, default=True)
    role: Mapped[str]= mapped_column(String, server_default="user")
    phone_number: Mapped[str]= mapped_column(String, nullable=True)

    todos: Mapped[List["Todos"]]= relationship(
        back_populates="users",
        cascade="all, delete-orphan",
    )

class Todos(Base):
    __tablename__= "todos"

    id: Mapped[int]= mapped_column(Integer, primary_key= True, autoincrement=True, index=True)
    title: Mapped[str]= mapped_column(String(50), nullable= False)
    description: Mapped[str]= mapped_column(String(100))
    priority: Mapped[int]= mapped_column(Integer, nullable= False)
    completed: Mapped[bool]= mapped_column(Boolean, default=False)
    owner: Mapped[int]= mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    __table_args__= (
        CheckConstraint("priority >= 1 AND priority <= 5", name= "check_priority_range"),
    )

    users: Mapped[List["Users"]]= relationship(
        back_populates="todos",
    )

    # ORM Level validation
    @validates("priority") #which mapped_column this decorator is validating.
    def validate_priority_range(self, key, value):
        if value is not None and not (1 <= value <=5):
            raise ValueError("priority must be between 1 and 5")
        return value