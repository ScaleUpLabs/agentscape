from sqlmodel import Field, SQLModel
from uuid import uuid4
from typing import Optional
import sqlalchemy as sa

class Agent(SQLModel, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    description: str
    endpoint: str = Field(sa_type=sa.String)
    openapi_url: Optional[str] = Field(default=None, sa_type=sa.String)
    org_website: str = Field(sa_type=sa.String)
    org_email: str = Field(sa_type=sa.String)
    tags: Optional[str] = None