from pydantic import BaseModel, HttpUrl, EmailStr
from typing import List, Optional

class AgentCreate(BaseModel):
    name: str
    description: str
    endpoint: HttpUrl
    openapi_url: Optional[HttpUrl] = None
    org_website: HttpUrl
    org_email: EmailStr
    tags: Optional[List[str]] = []

class AgentRead(BaseModel):
    id: str
    name: str
    description: str
    endpoint: HttpUrl
    openapi_url: Optional[HttpUrl] = None
    org_website: HttpUrl
    org_email: EmailStr
    tags: Optional[List[str]] = []

class MCPManifest(BaseModel):
    name: str
    description: str
    version: Optional[str] = "1.0"
    contact: Optional[dict] = None
    api: dict
    entrypoint: HttpUrl
    auth: Optional[dict] = None
    tags: Optional[List[str]] = []