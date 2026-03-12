from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = None
    database_hostname: str = None
    database_port: str = None
    database_password: str = None
    database_name: str = None
    database_user: str = None
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    class Config:
        env_file = ".env"

settings = Settings()
