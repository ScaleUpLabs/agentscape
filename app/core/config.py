import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    csv_file_name: str = "agents.csv"  # Default value, will be overridden by .env
    api_title: str = "AgentScape: Agent White Pages"
    api_description: str = "Agent registry service for MCP compatible agents"
    debug: bool = True

    class Config:
        env_file = ".env"
        case_sensitive = False  # Makes the settings case-insensitive

    @property
    def csv_path(self) -> str:
        # Ensure directory exists
        csv_path = Path(self.csv_file_name)
        if csv_path.parent != Path('.'):
            os.makedirs(csv_path.parent, exist_ok=True)
        return str(csv_path)

settings = Settings()