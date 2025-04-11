import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    sqlite_file_name: str = "test.db"  # Default value, will be overridden by .env
    api_title: str = "AgentScape: Agent White Pages"
    api_description: str = "Agent registry service for MCP compatible agents"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False  # Makes the settings case-insensitive

    @property
    def sqlite_url(self) -> str:
        # Ensure directory exists
        db_path = Path(self.sqlite_file_name)
        if db_path.parent != Path('.'):
            os.makedirs(db_path.parent, exist_ok=True)
        return f"sqlite:///{self.sqlite_file_name}"

settings = Settings()