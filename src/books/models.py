from sqlmodel import SQLModel,Field, Column
from datetime import datetime,date
from uuid import UUID
from typing import Optional
import uuid
import sqlalchemy.dialects.postgresql as pg
from src.db.models import User
from sqlmodel import Relationship
class Book(SQLModel, table = True ):
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

    def __repr__(self):
        return f"<Book{self.title}>"
    
# now just creating the models does not do the job
# we need to craete the table in the databease so what we do is make this in intit_db ie 
# add the creation of this table in init db 