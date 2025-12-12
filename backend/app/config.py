from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryBrain AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/factorybrain"
    REDIS_URL: str = "redis://localhost:6379"
    
    ELEVENLABS_API_KEY: str = ""
    CEREBRAS_API_KEY: str = ""
    ANTHROPIC_API_KEY: str = ""
    
    RAINDROP_BUCKET_ENDPOINT: str = ""
    RAINDROP_SQL_ENDPOINT: str = ""
    RAINDROP_MEMORY_ENDPOINT: str = ""
    RAINDROP_INFERENCE_ENDPOINT: str = ""
    
    VULTR_KUBERNETES_ENDPOINT: str = ""
    VULTR_OBJECT_STORAGE_ENDPOINT: str = ""
    VULTR_ACCESS_KEY: str = ""
    VULTR_SECRET_KEY: str = ""
    
    IOT_BROKER_HOST: str = "localhost"
    IOT_BROKER_PORT: int = 1883
    
    ANOMALY_THRESHOLD: float = 0.75
    ENERGY_OPTIMIZATION_MODE: bool = True
    CO2_REDUCTION_TARGET: float = 0.20
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()