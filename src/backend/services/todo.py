from sqlalchemy.orm import Session
from database.models import Todos

class ToDo:

    # GET Operations

    def todo_list_all(db:Session):
        return db.query(Todos).all()

    def todo_by_id(db: Session, todo_id:int):
        return db.query(Todos).filter(Todos.id==todo_id).first()

    def user_todo_list(db: Session, owner_id: int):
        return db.query(Todos).filter(Todos.owner==owner_id).all()


    # POST Operations

    def create_todo(db: Session, body, owner_id: int):
        todo_model = Todos(**body.model_dump())
        todo_model.owner= owner_id

        db.add(todo_model)
        db.commit()
        return


    # PUT Operations

    def update_todo(db: Session, body, todo_id: int, owner_id: int):
        todo_model= db.query(Todos).filter((Todos.owner==owner_id) & (Todos.id==todo_id)).first()
        if todo_model is None:
            return False
        updates = body.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in updates.items():
            setattr(todo_model, field, value)
        
        db.commit()
        return True


    # DELETE Operations

    def delete_todo(db: Session, todo_id: int, owner_id: int):
        todo_model=db.query(Todos).filter((Todos.owner==owner_id) & (Todos.id==todo_id)).first()

        if todo_model is None:
            return False
        db.query(Todos).filter((Todos.owner==owner_id) & (Todos.id==todo_id)).delete()
        db.commit()
        return True