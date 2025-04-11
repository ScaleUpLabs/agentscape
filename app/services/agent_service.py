from sqlmodel import Session
from models.agent import Agent
from schemas.agent import AgentCreate
from fastapi import HTTPException
from urllib.parse import urlparse
import httpx

def verify_domain_match(endpoint_url: str, org_website: str, org_email: str) -> bool:
    endpoint_domain = urlparse(endpoint_url).netloc
    website_domain = urlparse(org_website).netloc
    email_domain = org_email.split("@")[1]
    return (endpoint_domain.endswith(website_domain)
            and email_domain == website_domain)

def register_agent(agent: AgentCreate, session: Session) -> Agent:
    if not verify_domain_match(str(agent.endpoint), str(agent.org_website), agent.org_email):
        raise HTTPException(status_code=400, detail="Domain mismatch between endpoint, website, and email")

    agent_obj = Agent(**agent.dict(), tags=','.join(agent.tags or []))
    session.add(agent_obj)
    session.commit()
    session.refresh(agent_obj)
    return agent_obj

def register_from_manifest(manifest_data: dict, session: Session) -> Agent:
    contact = manifest_data.get("contact", {})
    org_website = contact.get("url")
    org_email = contact.get("email")

    if not org_website or not org_email:
        raise HTTPException(status_code=400, detail="Manifest must include contact.url and contact.email")

    if not verify_domain_match(str(manifest_data['entrypoint']), str(org_website), org_email):
        raise HTTPException(status_code=400, detail="Domain mismatch between entrypoint, website, and email")

    agent = Agent(
        name=manifest_data['name'],
        description=manifest_data['description'],
        endpoint=manifest_data['entrypoint'],
        openapi_url=manifest_data['api'].get("url"),
        org_website=org_website,
        org_email=org_email,
        tags=','.join(manifest_data.get('tags', []))
    )

    session.add(agent)
    session.commit()
    session.refresh(agent)
    return agent

def list_agents(session: Session, name: str = None, org_email: str = None, org_website: str = None, tag: str = None):
    query = select(Agent)
    if name:
        query = query.where(Agent.name.ilike(f"%{name}%"))
    if org_email:
        query = query.where(Agent.org_email == org_email)
    if org_website:
        query = query.where(Agent.org_website == org_website)
    if tag:
        query = query.where(Agent.tags.contains(tag))
    return session.exec(query).all()

def get_agent(agent_id: str, session: Session) -> Agent:
    agent = session.get(Agent, agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent