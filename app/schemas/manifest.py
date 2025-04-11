from pydantic import BaseModel, HttpUrl, EmailStr
from typing import Optional, List

class MCPManifest(BaseModel):
    name: str
    description: str
    version: Optional[str] = "1.0"
    contact: Optional[dict] = None
    api: dict
    entrypoint: HttpUrl
    auth: Optional[dict] = None
    tags: Optional[List[str]] = []