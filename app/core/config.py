from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Classe para gerenciar as configurações da aplicação.
    As variáveis são carregadas de um arquivo .env.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")
    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


settings = Settings()
