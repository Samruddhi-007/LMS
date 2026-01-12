"""
Application Configuration
Manages environment variables and settings using Pydantic
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    APP_NAME: str = "LMS Backend"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"
    SECRET_KEY: str = "your-secret-key-change-this"
    
    # Server
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database
    DATABASE_URL: str
    DB_POOL_SIZE: int = 10
    DB_MAX_OVERFLOW: int = 20
    
    # CORS (comma-separated string)
    CORS_ORIGINS: str = "http://localhost:3000,http://localhost:5173"
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as list"""
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 2097152  # 2MB
    MAX_IMAGE_SIZE: int = 1048576  # 1MB
    ALLOWED_IMAGE_TYPES: str = "image/jpeg,image/png,image/jpg"
    ALLOWED_DOCUMENT_TYPES: str = "application/pdf"
    
    # Storage
    STORAGE_TYPE: str = "local"  # local or s3
    AWS_ACCESS_KEY_ID: str = ""
    AWS_SECRET_ACCESS_KEY: str = ""
    AWS_REGION: str = ""
    AWS_BUCKET_NAME: str = ""
    
    # JWT (if using authentication)
    JWT_SECRET_KEY: str = "your-jwt-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra='ignore'  # Ignore extra fields in .env
    )
    
    @property
    def allowed_image_types_list(self) -> List[str]:
        """Get allowed image types as list"""
        return [t.strip() for t in self.ALLOWED_IMAGE_TYPES.split(",")]
    
    @property
    def allowed_document_types_list(self) -> List[str]:
        """Get allowed document types as list"""
        return [t.strip() for t in self.ALLOWED_DOCUMENT_TYPES.split(",")]


# Create settings instance
settings = Settings()
