from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Gas Cylinder Booking System"
    PROJECT_VERSION: str = "1.0.0"
    
    # Database configuration
    DATABASE_URL: str = "sqlite:///./gas_cylinder_booking.db"
    
    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email Settings (for notifications)
    SMTP_SERVER: str = ""
    SMTP_PORT: int = 587
    SMTP_USERNAME: str = ""
    SMTP_PASSWORD: str = ""
    
    class Config:
        env_file = ".env"

settings = Settings()
