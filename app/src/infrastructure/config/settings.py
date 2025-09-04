import os
from typing import Optional
try:
    from pydantic_settings import BaseSettings
except ImportError:
    from pydantic import BaseSettings
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings(BaseSettings):
    """
    Configurações da aplicação.
    
    Aplicando o princípio Single Responsibility Principle (SRP) - 
    responsável apenas pela gestão de configurações.
    
    Todas as configurações são centralizadas aqui e podem ser
    sobrescritas por variáveis de ambiente.
    """
    
    # Database settings
    db_user: str = os.getenv("DB_USER", "carsales_user")
    db_password: str = os.getenv("DB_PASSWORD", "Mudar123!")
    db_host: str = os.getenv("DB_HOST", "db-carsales")
    db_port: str = os.getenv("DB_PORT", "3306")
    db_name: str = os.getenv("DB_NAME", "carsales")
    
    # JWT settings
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "your-secret-key-here-change-in-production")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Application settings
    app_name: str = os.getenv("APP_NAME", "Car Sales API")
    app_version: str = os.getenv("APP_VERSION", "1.0.0")
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    
    # Logging settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    sql_echo: bool = os.getenv("SQL_ECHO", "False").lower() == "true"
    
    # File upload settings
    upload_dir: str = os.getenv("UPLOAD_DIR", "static/uploads")
    max_file_size: int = int(os.getenv("MAX_FILE_SIZE", "10485760"))  # 10MB
    allowed_extensions: list = [".jpg", ".jpeg", ".png", ".gif"]
    
    @property
    def database_url(self) -> str:
        """
        Constrói a URL de conexão com o banco de dados.
        
        Returns:
            str: URL de conexão com o banco
        """
        return f"mysql+pymysql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Instância global das configurações
settings = Settings()
