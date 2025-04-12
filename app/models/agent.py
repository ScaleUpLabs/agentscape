from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

class Agent(BaseModel):
    id: Optional[str] = None
    name: str
    description: str
    endpoint: str
    openapi_url: Optional[str] = None
    org_website: str
    org_email: str
    tags: Optional[str] = None
    
    def dict(self):
        return {
            'id': self.id or str(uuid4()),
            'name': self.name,
            'description': self.description,
            'endpoint': self.endpoint,
            'openapi_url': self.openapi_url,
            'org_website': self.org_website,
            'org_email': self.org_email,
            'tags': self.tags or ''
        }