from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date,datetime
from typing import Optional
from sqlmodel import Relationship

from sqlmodel import SQLModel,Field, Column
from datetime import datetime,date
from uuid import UUID
from typing import Optional,List
import uuid
import sqlalchemy.dialects.postgresql as pg
from sqlmodel import Relationship
class User(SQLModel, table=True):
    __tablename__ = "user_accounts"#type:ignore

    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            primary_key=True,
            unique=True,
            nullable=False,
            default=uuid.uuid4,
            info={"description": "Unique identifier for the user account"},
        )
    )
    role: str = Field(
        sa_column=Column(pg.VARCHAR, nullable=False, server_default="user")
    ) 
    username: str
    first_name: str = Field(nullable=True)
    last_name: str = Field(nullable=True)
    is_verified: bool = False
    email: str
    password_hash: str = Field(exclude = True )
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at :datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    reviews: List["Reviews"] = Relationship(back_populates="user",sa_relationship_kwargs={'lazy':'selectin'})
    books: List["Book"] = Relationship(back_populates="user",sa_relationship_kwargs={'lazy':'selectin'})
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    

class Book(SQLModel, table = True ):
    __tablename__ = "books"#type:ignore
    uid : UUID = Field(
      sa_column=Column (
          pg.UUID ,
          nullable = False ,
          primary_key = True ,
          default = uuid.uuid4
      )
    ) 
    title : str 
    author : str 
    publisher: str  
    published_date : date 
    user_uid:Optional[uuid.UUID] = Field(default = None ,foreign_key="user_accounts.uid")
    page_count : int 
    language : str 
    created_at : datetime= Field(sa_column=Column(pg.TIMESTAMP,default = datetime.now()))
    updated_at : datetime= Field(sa_column=Column(pg.TIMESTAMP,default = datetime.now()))
    user : Optional["User"]=Relationship(back_populates="books")
    reviews: List["Reviews"] = Relationship(back_populates="books",sa_relationship_kwargs={'lazy':'selectin'})
    tags: List["Tag"] = Relationship(
    back_populates="books",
    sa_relationship_kwargs={
        "lazy": "selectin"
    }
)
    def __repr__(self):
        return f"<Book{self.title}>"
    
# now just creating the models does not do the job
# we need to craete the table in the databease so what we do is make this in intit_db ie 
# add the creation of this table in init db 


class Reviews(SQLModel, table = True ):
    uid : UUID = Field(
      sa_column=Column (
          pg.UUID ,
          nullable = False ,
          primary_key = True ,
          default = uuid.uuid4
      )
    ) 
    user_uid:Optional[uuid.UUID] = Field(default = None ,foreign_key="user_accounts.uid")
    book_uid:Optional[uuid.UUID] = Field(default = None ,foreign_key="books.uid")
    rating : int = Field(lt= 5) 
    review_text:str
    created_at : datetime= Field(sa_column=Column(pg.TIMESTAMP,default = datetime.now()))
    updated_at : datetime= Field(sa_column=Column(pg.TIMESTAMP,default = datetime.now()))
    user : Optional["User"]=Relationship(back_populates="reviews")


    def __repr__(self):
        return f"<Review{self.book_uid} by {self.user_uid}>"


class BookTag(SQLModel, table=True):
    book_id: uuid.UUID = Field(default=None, foreign_key="books.uid", primary_key=True)
    tag_id: uuid.UUID = Field(default=None, foreign_key="tags.uid", primary_key=True)


class Tag(SQLModel, table=True):
    __tablename__ = "tags"#type:ignore
    uid: uuid.UUID = Field(
        sa_column=Column(pg.UUID, nullable=False, primary_key=True, default=uuid.uuid4)
    )
    name: str = Field(sa_column=Column(pg.VARCHAR, nullable=False))
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    books: List["Book"] = Relationship(
        link_model=BookTag,
        back_populates="tags",
        sa_relationship_kwargs={"lazy": "selectin"},
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"
 