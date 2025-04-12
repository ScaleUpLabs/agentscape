from pydantic import BaseModel, Field, field_validator
from typing import Optional
from uuid import uuid4

class Agent(BaseModel):
    id: Optional[str] = None
    name: str = Field(..., description="Name of the agent")
    description: str = Field(..., description="Description of the agent")
    endpoint: str = Field(..., description="API endpoint URL of the agent")
    openapi_url: str = Field(..., description="OpenAPI specification URL")
    org_website: str = Field(..., description="Organization website URL")
    org_email: str = Field(..., description="Organization email address")
    tags: Optional[str] = None
    
    @field_validator("name", "description", "endpoint", "org_website", "org_email", mode='before')
    def check_required_fields(cls, value, info):
        if not value or (isinstance(value, str) and value.strip() == ""):
            field_name = info.field_name
            raise ValueError(f"The field '{field_name}' is required and cannot be empty.")
        return value
    
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