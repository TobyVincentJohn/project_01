from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter()

# Pydantic models for request/response
class AgentCreate(BaseModel):
    name: str
    description: Optional[str] = None
    industry: Optional[str] = None
    product_details: Optional[str] = None
    target_audience: Optional[str] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    industry: Optional[str] = None
    product_details: Optional[str] = None
    target_audience: Optional[str] = None

# Create agent
@router.post("/")
async def create_agent(agent: AgentCreate):
    return {
        "message": "Agent created successfully",
        "agent": agent.dict()
    }

# Get all agents
@router.get("/")
async def get_agents():
    return {
        "agents": [
            {
                "id": 1,
                "name": "Test Agent",
                "description": "Test Description",
                "industry": "Technology"
            }
        ]
    }

# Get single agent
@router.get("/{agent_id}")
async def get_agent(agent_id: int):
    return {
        "id": agent_id,
        "name": "Test Agent",
        "description": "Test Description",
        "industry": "Technology"
    }

# Update agent
@router.put("/{agent_id}")
async def update_agent(agent_id: int, agent: AgentUpdate):
    return {
        "message": "Agent updated successfully",
        "agent_id": agent_id,
        "updated_data": agent.dict(exclude_unset=True)
    }

# Delete agent
@router.delete("/{agent_id}")
async def delete_agent(agent_id: int):
    return {
        "message": f"Agent {agent_id} deleted successfully"
    } 