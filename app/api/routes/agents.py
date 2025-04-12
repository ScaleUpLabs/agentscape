from fastapi import APIRouter, HTTPException, Body, Query, Depends, Request
from typing import List, Optional
from models.agent import Agent
from schemas.agent import AgentCreate, AgentRead
from services.agent_service import verify_domain_match, register_agent, list_agents, get_agent as get_agent_service
from db.database import get_db, CSVDatabase
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

def _prepare_agent_response(agent: Agent) -> dict:
    """Convert database Agent model to a dict compatible with AgentRead schema."""
    agent_dict = agent.dict()
    # Convert tags from string to list
    if agent.tags and isinstance(agent.tags, str):
        agent_dict["tags"] = agent.tags.split(",") if agent.tags else []
    else:
        agent_dict["tags"] = []
    return agent_dict

@router.post("/", response_model=AgentRead)
@limiter.limit("5/minute")
def create_agent(request: Request, agent: AgentCreate, db: CSVDatabase = Depends(get_db)) -> dict:
    agent_obj = register_agent(agent, db)
    
    # Prepare response
    return _prepare_agent_response(agent_obj)

@router.get("/", response_model=List[AgentRead])
@limiter.limit("20/minute")
def get_agents(
    request: Request,
    name: Optional[str] = Query(None),
    org_email: Optional[str] = Query(None),
    org_website: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: CSVDatabase = Depends(get_db)
) -> List[dict]:
    results = list_agents(db, name, org_email, org_website, tag)
    
    # Convert each agent for response
    return [_prepare_agent_response(agent) for agent in results]

@router.get("/{agent_id}", response_model=AgentRead)
@limiter.limit("10/minute")
def get_agent(request: Request, agent_id: str, db: CSVDatabase = Depends(get_db)) -> dict:
    agent = get_agent_service(agent_id, db)
    
    # Prepare response
    return _prepare_agent_response(agent)