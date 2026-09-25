from sqlalchemy.orm import Session
from database.models import Users, Todos

class User:

    # GET Operations

    def get_user_list(db: Session):
        return db.query(Users).all()

    def get_user_by_id(db: Session, id: int):
        return db.query(Users).filter(Users.id==id).first()
        
    def get_user_todo_list(db: Session, id: int):
        user= db.query(Users).filter(Users.id==id).first()
        if user is None:
            return None, None
        
        todo_list= db.query(Todos).filter(Todos.owner==id).all()
        return user, todo_list


    # POST Operations

    def add_user(db: Session, body):
        user_model= Users(**body.model_dump())

        db.add(user_model)
        db.commit()
        return True


    # PUT Operations

    def update_user(db: Session, id: int, body):
        user_model= db.query(Users).filter(Users.id==id).first()
        if user_model is None:
            return False

        updates = body.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in updates.items():
            setattr(user_model, field, value)

        db.commit()
        return True


    # DELETE Operations

    def delete_user(db:Session, id: int):
        deleted=db.query(Users).filter(Users.id==id).first()
        if deleted is None:
            return False
        db.query(Users).filter(Users.id==id).delete()
        db.commit()
        return True