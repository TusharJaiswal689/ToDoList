from sqlalchemy.orm import Session
from database.models import Users, Todos
from backend.services import auth
from sqlalchemy.exc import IntegrityError

class User:

    # GET Operations

    def get_user_list(db: Session):
        return db.query(Users).all()

    def get_user_by_id(db: Session, id: int):
        return db.query(Users).filter(Users.id==id).first()


    # POST Operations

    def add_user(db: Session, body):
        existing_user = (
            db.query(Users).filter(
                (Users.username==body.username)
                |(Users.email==body.email)
            ).first()
        )

        if existing_user:
            return False, "Username or Email already exists."

        user_data= body.model_dump()
        plain_password= user_data.pop("password")
        user_model=Users(**user_data)
        user_model.hashed_password=auth.hash_password(plain_password)

        db.add(user_model)
        try:
            db.commit()
        except IntegrityError:
            db.rollback()
            return False, "Username or Email already exists."
        return True,None


    # PUT Operations

    def update_user(db: Session, body, id):
        user_model= db.query(Users).filter(Users.id==id).first()
        if user_model is None:
            return False

        updates = body.model_dump(exclude_unset=True, exclude_none=True)

        for field, value in updates.items():
            setattr(user_model, field, value)

        db.commit()
        return True

    def update_user_password(db: Session, plain_password: str, id: int):
        user_model=db.query(Users).filter(Users.id==id).first()
        if user_model is None:
            return False
        user_model.hashed_password=auth.hash_password(plain_password)

        db.commit()
        return True


    # DELETE Operations

    def delete_user(db:Session, id: int):
        user=db.query(Users).filter(Users.id==id).first()
        if user is None:
            return False
        db.delete(user)
        db.commit()
        return True