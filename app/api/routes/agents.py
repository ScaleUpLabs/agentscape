from fastapi import APIRouter, HTTPException, Body, Query, Depends, Request
from typing import List, Optional
from sqlmodel import Session, select
from models.agent import Agent
from schemas.agent import AgentCreate, AgentRead
from services.agent_service import verify_domain_match
from db.database import get_db
from slowapi import Limiter
from slowapi.util import get_remote_address

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

def _prepare_agent_response(agent: Agent) -> dict:
    """Convert database Agent model to a dict compatible with AgentRead schema."""
    agent_dict = agent.__dict__
    # Convert tags from string to list
    if agent.tags and isinstance(agent.tags, str):
        agent_dict["tags"] = agent.tags.split(",") if agent.tags else []
    else:
        agent_dict["tags"] = []
    return agent_dict

@router.post("/", response_model=AgentRead)
@limiter.limit("5/minute")
def register_agent(request: Request, agent: AgentCreate, db: Session = Depends(get_db)) -> dict:
    if not verify_domain_match(str(agent.endpoint), str(agent.org_website), agent.org_email):
        raise HTTPException(status_code=400, detail="Domain mismatch between endpoint, website, and email")

    # Convert to dictionary and update all fields properly
    agent_dict = agent.dict()
    agent_dict["endpoint"] = str(agent.endpoint)
    agent_dict["org_website"] = str(agent.org_website)
    if agent.openapi_url:
        agent_dict["openapi_url"] = str(agent.openapi_url)
    agent_dict["tags"] = ','.join(agent.tags or [])
    
    agent_obj = Agent(**agent_dict)
    db.add(agent_obj)
    db.commit()
    db.refresh(agent_obj)
    
    # Prepare response
    return _prepare_agent_response(agent_obj)

@router.get("/", response_model=List[AgentRead])
@limiter.limit("20/minute")
def list_agents(
    request: Request,
    name: Optional[str] = Query(None),
    org_email: Optional[str] = Query(None),
    org_website: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    db: Session = Depends(get_db)
) -> List[dict]:
    query = select(Agent)
    if name:
        query = query.where(Agent.name.ilike(f"%{name}%"))
    if org_email:
        query = query.where(Agent.org_email == org_email)
    if org_website:
        query = query.where(Agent.org_website == org_website)
    if tag:
        query = query.where(Agent.tags.contains(tag))
    results = db.exec(query).all()
    
    # Convert each agent for response
    return [_prepare_agent_response(agent) for agent in results]

@router.get("/{agent_id}", response_model=AgentRead)
@limiter.limit("10/minute")
def get_agent(request: Request, agent_id: str, db: Session = Depends(get_db)) -> dict:
    agent = db.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Prepare response
    return _prepare_agent_response(agent)