from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    MODE: str

    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_PORT: int
    DB_SERVER: str

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_SERVER}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = '.env'


settings = Settings()

# DB_URL = 'postgresql+asyncpg://postgres:password@localhost:5432/postgres'
# DB_URL = 'postgresql+asyncpg://postgres:password@db/postgres'
