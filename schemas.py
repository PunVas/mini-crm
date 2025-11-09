from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Lead Schemas
class LeadBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    company: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = None
    status: str = Field(default="New", pattern="^(New|Interested|In Progress|Closed|Lost)$")

class LeadCreate(LeadBase):
    pass

class LeadUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    company: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    status: Optional[str] = Field(None, pattern="^(New|Interested|In Progress|Closed|Lost)$")

class Lead(LeadBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Interaction Schemas
class InteractionBase(BaseModel):
    interaction_type: str = Field(..., pattern="^(Call|Email|Meeting)$")
    notes: Optional[str] = None

class InteractionCreate(InteractionBase):
    lead_id: int

class Interaction(InteractionBase):
    id: int
    lead_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Response schemas
class LeadWithInteractions(Lead):
    interactions: List[Interaction] = []
    
    class Config:
        from_attributes = True