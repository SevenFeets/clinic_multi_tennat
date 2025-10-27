"""
Configuration settings for the application

🎯 YOUR MISSION (Week 1):
Load environment variables from .env file and make them available to your app

📚 LEARNING RESOURCES:
- Pydantic Settings: https://docs.pydantic.dev/latest/usage/pydantic_settings/
- Environment Variables: https://www.youtube.com/watch?v=IolxqkL7cD8

💡 HINTS:
- Use pydantic_settings to load environment variables
- This is safer than using os.getenv() directly
- BaseSettings automatically loads from .env file
"""

# TODO: Import necessary modules
# HINT: from pydantic_settings import BaseSettings
# HINT: from pydantic import Field


# TODO: Create a Settings class that inherits from BaseSettings
# HINT: class Settings(BaseSettings):

    # TODO: Define configuration variables
    # HINT: database_url: str = Field(..., env="DATABASE_URL")
    # HINT: secret_key: str = Field(..., env="SECRET_KEY")
    # HINT: algorithm: str = Field(default="HS256", env="ALGORITHM")
    # HINT: access_token_expire_minutes: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # TODO: Add a nested Config class
    # HINT: class Config:
    # HINT:     env_file = ".env"
    # HINT:     case_sensitive = False


# TODO: Create a settings instance
# HINT: settings = Settings()


# 🎯 CHALLENGE:
# Add validation to ensure DATABASE_URL starts with "postgresql://"
# HINT: Use Pydantic's @validator decorator

# 🧪 TESTING:
# In Python console: 
# >>> from app.config import settings
# >>> print(settings.database_url)

