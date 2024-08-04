from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column
import uuid

Base = declarative_base()

def generate_uuid():
    return str(uuid.uuid4())


class User(Base):
    __tablename__ = "users"
    id = Column('id', String(50), primary_key=True, default = generate_uuid)
    name = Column('name', String(50))
    age = Column('age', Integer)

    def __init__(self, name, age):
        self.name = name
        self.age = age

engine = create_engine("sqlite:///socialDB.db", echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

def addUser(name, age, session):

    user = User(name, age)
    session.add(user)
    session.commit()
    print('User added to the db')
        
name = "hello"
age = 22

# addUser(name, age, session)

# Retrieve all records from the User table.
def retrieve_entries(User, session):
    entries = session.query(User).all()
    all_entries = []
    for p in entries:
        all_entries.append(p.name)
        all_entries.append(p.age)
    # session.commit() ##commiting after read operations is not neccessary. only after, inser, modify and delete
    return all_entries

# print(retrieve_entries(User, session))

def retrieve_by_age(User, age, session):
    users_above_age = []
    entries = session.query(User).filter(User.age > age).all()
    for p in entries:
        users_above_age.append(p.name)
    # session.commit()
    return users_above_age

# print(retrieve_by_age(User, 25, session))

#update user
def update_user_age(session, User, name, new_age):
    session.query(User).filter(User.name == name).update({"age": new_age})
    session.commit()
    print(f'User {name} updated to age {new_age}')

#delete user
def delete_user(session, User, name):
    session.query(User).filter(User.name == name).delete()
    session.commit()
    print(f'User {name} deleted')

update_user_age(session, User, 'Paco', 31)

delete_user(session, User, 'lala')

entries = session.query(User).all()
for p in entries:
    print(p.name)
    print(p.age)
    
session.close()