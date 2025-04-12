from models.agent import Agent
from schemas.agent import AgentCreate
from fastapi import HTTPException
from urllib.parse import urlparse
from db.database import CSVDatabase
from typing import List, Optional

def verify_domain_match(endpoint_url: str, org_website: str, org_email: str) -> bool:
    endpoint_domain = urlparse(endpoint_url).netloc
    website_domain = urlparse(org_website).netloc
    email_domain = org_email.split("@")[1]
    return (endpoint_domain.endswith(website_domain)
            and email_domain == website_domain)

def register_agent(agent: AgentCreate, db: CSVDatabase) -> Agent:
    if not verify_domain_match(str(agent.endpoint), str(agent.org_website), agent.org_email):
        raise HTTPException(status_code=400, detail="Domain mismatch between endpoint, website, and email")

    # Convert AgentCreate to a dictionary and convert URLs to strings
    agent_data = {
        'name': agent.name,
        'description': agent.description,
        'endpoint': str(agent.endpoint),  # Convert HttpUrl to string
        'openapi_url': str(agent.openapi_url) if agent.openapi_url else None,  # Convert optional HttpUrl to string
        'org_website': str(agent.org_website),  # Convert HttpUrl to string
        'org_email': agent.org_email,
        'tags': ','.join(agent.tags or [])
    }
    
    # Add the agent to CSV database
    db_dict = db.add(agent_data)
    
    # Convert back to Agent model
    return Agent(**db_dict)

def register_from_manifest(manifest_data: dict, db: CSVDatabase) -> Agent:
    contact = manifest_data.get("contact", {})
    org_website = contact.get("url")
    org_email = contact.get("email")

    if not org_website or not org_email:
        raise HTTPException(status_code=400, detail="Manifest must include contact.url and contact.email")

    if not verify_domain_match(str(manifest_data['entrypoint']), str(org_website), org_email):
        raise HTTPException(status_code=400, detail="Domain mismatch between entrypoint, website, and email")

    agent_data = {
        'name': manifest_data['name'],
        'description': manifest_data['description'],
        'endpoint': str(manifest_data['entrypoint']),
        'openapi_url': str(manifest_data['api'].get("url")) if manifest_data['api'].get("url") else None,
        'org_website': str(org_website),
        'org_email': org_email,
        'tags': ','.join(manifest_data.get('tags', []))
    }
    
    # Add the agent to CSV database
    db_dict = db.add(agent_data)
    
    # Convert back to Agent model
    return Agent(**db_dict)

def list_agents(db: CSVDatabase, name: str = None, org_email: str = None, org_website: str = None, tag: str = None) -> List[Agent]:
    filter_args = {}
    
    if name:
        filter_args['name__ilike'] = f"%{name}%"
    if org_email:
        filter_args['org_email'] = org_email
    if org_website:
        filter_args['org_website'] = org_website
    if tag:
        filter_args['tags__contains'] = tag
        
    results = db.filter(**filter_args)
    return [Agent(**record) for record in results]

def get_agent(agent_id: str, db: CSVDatabase) -> Agent:
    agent_data = db.get_by_id(agent_id)
    if not agent_data:
        raise HTTPException(status_code=404, detail="Agent not found")
    return Agent(**agent_data)