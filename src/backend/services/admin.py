from sqlalchemy.orm import Session
from database.models import Users, Todos

class Admin:
    def todo_list_all(db:Session):
            return db.query(Todos).all()

    def todo_by_id(db: Session, todo_id:int):
        return db.query(Todos).filter(Todos.id==todo_id).first()

    def get_user_list(db: Session):
        return db.query(Users).all()
    
    def get_user_by_id(db: Session, id: int):
        return db.query(Users).filter(Users.id==id).first()