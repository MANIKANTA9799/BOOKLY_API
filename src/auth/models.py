from sqlmodel import SQLModel, Field, Column
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import date,datetime
from typing import Optional
from sqlmodel import Relationship
from src.db.models import Book
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
    books: Optional["Book"] = Relationship(back_populates="user",sa_relationship_kwargs={'lazy':'selectin'})
    def __repr__(self) -> str:
        return f"<User {self.username}>"
    



