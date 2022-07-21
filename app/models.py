from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from .database import Base


class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    '''relationship automatically creates another property for File, so when we retrieve 
    File it will return an 'owner' property too, and it will figure out the relationship to   
    User. Basically, will fetch the User based of the owner id and return that for us
    Example of data response with relationship:
    {
        "id": 12,
        "file": "",
        "file_title": "dfasdf",
        "patient_id": 3434,
        "user_id": 4545,
        "owner": {
            "id": 223,
            "email": "john@hotmail.com",
            "password": "fadfaf",
            "created_at": "2022"
        }
    }
    Use pydantic models in path operations to limit the data. For example changing the data
    format to only id and email, excluding the password and created_at properties.
    '''

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    phone_number = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
