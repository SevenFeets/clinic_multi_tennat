
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    app_name: str = "Clinic Management SaaS"
    debug: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False
    )

    @field_validator('database_url')
    def validate_database_url(cls, v):
        if not v.startswith("postgresql://") and not v.startswith("sqlite://"):
            raise ValueError("DATABASE_URL must start with postgresql:// or sqlite://")
        return v

    
    @field_validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v


    @field_validator('access_token_expire_minutes')
    def validate_access_token_expire_minutes(cls, v):
        if v < 1 or v > 1440:
            raise ValueError("ACCESS_TOKEN_EXPIRE_MINUTES must be between 1 and 1440 minutes")
        return v


    @field_validator('algorithm')
    def validate_algorithm(cls, v):
        if v not in ["HS256", "RS256"]:
            raise ValueError("ALGORITHM must be either HS256 or RS256")
        return v


    @field_validator('app_name')
    def validate_app_name(cls, v):
        if len(v) < 1:
            raise ValueError("APP_NAME must be at least 1 character long")
        return v


# Create settings instance
settings = Settings()



