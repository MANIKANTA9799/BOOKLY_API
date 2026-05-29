# the puprpose of this file to help acees teh env variavles and provide to 
# mian prog 
# pydantic settings helps provide ways for 
# config file to interact with the .env file
# setting config dict helps to set the env file we want toread from basciaclly 
# for this project 
# also the way the basesettings from the pydantic settungs loads the variables is 
# that it loops through the env file loads ones we are looking for in the place where we defined its name 
# ex if in env file we have db = "" here in this calss also db : type 


from pydantic_settings import BaseSettings, SettingsConfigDict
class Settings (BaseSettings):
    DATABASE_URL: str 
    JWT_SECRET :str 
    JWT_ALGORITHM :str
    REDIS_HOST : str 
    REDIS_PORT:int
    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
        # only load needed others dont care 
    )
Config = Settings()#type:ignore 