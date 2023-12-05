from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

DATABASE_URL = "postgresql://huawei:1@localhost/users"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class User(Base): 
    __tablename__ = "users"
    id = Column(Integer,primary_key =True, autoincrement=True)
    name = Column(String)
    last_name = Column(String)
    age = Column(Integer)

    def __init__(self, name, last_name, age):
        self.name = name
        self.last_name = last_name
        self.age = age

# Base.metadata.create_all(bind = engine)
# print('table created')

ItemPydentic = sqlalchemy_to_pydantic(User,exclude=["id"])


def create_user(name:ItemPydentic, last_name:ItemPydentic, age:ItemPydentic):
    user_data = ItemPydentic(name=name, last_name=last_name, age=age)
    with SessionLocal() as db:
        user = User(**user_data.dict())
        db.add(user)
        db.commit() 
        db.refresh(user)   
    return user

def get_user():
    result = []
    with SessionLocal() as db:
        db_user = db.query(User).all()
        for user in db_user:
            result.append({'name':user.name, 'last_name':user.last_name, 'age':user.age})
    return result

def update_user(user_id:int, new_name:str, new_last_name:str, new_age:int):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            user.name = new_name
            user.last_name = new_last_name
            user.age = new_age
            db.commit()
            db.refresh(user)
        return user
        
def delete_user(user_id:int):
    with SessionLocal() as db:
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
        return user


created_user = create_user(name='axl', last_name='bolt', age = 7)
# print('created:\n',created_user)

got_user = get_user()
# print('get_user:\n', got_user)

deleted_user = delete_user(user_id=2)
# print("DELETED USER\n", deleted_user)
# print('get_user:\n', got_user)

updated_user = update_user(user_id=3,new_name='Kise', new_last_name='Ryota', new_age=20)
# print(updated_user)
# print(got_user)





