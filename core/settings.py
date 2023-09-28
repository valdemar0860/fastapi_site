from pydantic_settings import BaseSettings 
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
print(BASE_DIR)


class Settings(BaseSettings):
    base_dir:str = str(BASE_DIR)
    db_url:str = f"sqlite+aiosqlite:///{base_dir}/data.db"
    db_echo:bool = True
    
settings = Settings()