import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Base de datos
    DATABASE_URL: str = "sqlite:///./consolidador.db"

    # SFTP GoAnywhere
    SFTP_HOST: str = "mft.positiva.gov.co"
    SFTP_PORT: int = 2243
    SFTP_USER: str = "G_medica"
    SFTP_PASSWORD: str = ""

    # Seguridad
    SECRET_KEY: str = "your-secret-key-change-in-production"
    DEBUG: bool = True

    # Directorios
    UPLOAD_DIR: str = "uploads"
    OUTPUT_DIR: str = "outputs"

    class Config:
        env_file = ".env"

settings = Settings()
