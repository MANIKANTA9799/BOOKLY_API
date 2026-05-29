from sqlmodel import create_engine,text,SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine 
from src.config import Config
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
# so the purpose of this file is to do something very unique it 
# helps to create engine that lietrally
#  manages all stuff od our datavnase like
#  maintaining session pool who has contro all tat shit 
from src.db.models import Book
async_engine = AsyncEngine(
    create_engine(
        url= Config.DATABASE_URL,
        echo  = True 
    )
)


async def init_db():
    async with async_engine.begin() as conn :
       await conn.run_sync(SQLModel.metadata.create_all)

       # here as we defined in model sql model , tabel = true so in sqlmodel meta data this stuff is stored
       # so here we need not explicitly call the  book or stufff as create all basically means create all 

async def get_session ()->AsyncSession: #type:ignore 
    Session  = sessionmaker (#type:ignore 
        bind = async_engine,#type:ignore 
        class_ = AsyncSession,
        expire_on_commit=False
    )
    async with Session() as session :#type:ignore 
        yield session#type:ignore 

# here echo is basically true means print all 
# the sql excuted in th consoek if false 
#do not print 


# so basiaclly we will look at something called as lifespan evenyts 
# when to start db at start 
# if app it becoms  heavy takes 
# time optimal start just bef start oif app
# how to acheive tjis use lifespan events syntax see below 
# one imp thing i forgot to say is that we need to have have await in async functios 
# for function call