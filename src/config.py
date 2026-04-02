from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path



class _Config:
    def __init__(self):
        self._root_dir:Path = Path("app")

    @property
    def root_dir(self) -> Path:
        return self._root_dir
    
    @root_dir.setter
    def root_dir(self, value: str | Path) -> None:
        self._root_dir = Path(value)



class _Settings(BaseSettings):
    auth_key:  str 
    algorithm: str
    access_token_expire_minutes: int

    model_config = SettingsConfigDict(env_file=".env")




config:   _Config   = _Config()
settings: _Settings = _Settings()