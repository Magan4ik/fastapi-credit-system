from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Middle Test Project"
    database_url: str
    debug: bool
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    auth2_scheme: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="auth/token")

    model_config = SettingsConfigDict(env_file='.env')


settings = Settings()
