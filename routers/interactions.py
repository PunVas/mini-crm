from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Lead, Interaction
from schemas import InteractionCreate, Interaction as InteractionSchema

router = APIRouter()

@router.post("/", response_model=InteractionSchema, status_code=201)
def create_interaction(interaction: InteractionCreate, db: Session = Depends(get_db)):
    """Create a new interaction for a lead"""
    # Check if the lead exists
    lead = db.query(Lead).filter(Lead.id == interaction.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Create the interaction
    db_interaction = Interaction(**interaction.model_dump())
    db.add(db_interaction)
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.get("/", response_model=List[InteractionSchema])
def get_interactions(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    lead_id: Optional[int] = None,
    interaction_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all interactions with optional filters"""
    query = db.query(Interaction)
    
    if lead_id:
        query = query.filter(Interaction.lead_id == lead_id)
    if interaction_type:
        query = query.filter(Interaction.interaction_type == interaction_type)
    
    interactions = query.offset(skip).limit(limit).all()
    return interactions

@router.get("/{interaction_id}", response_model=InteractionSchema)
def get_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Get a specific interaction by ID"""
    interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    return interaction

@router.put("/{interaction_id}", response_model=InteractionSchema)
def update_interaction(interaction_id: int, interaction_update: InteractionCreate, db: Session = Depends(get_db)):
    """Update an interaction"""
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    # Check if the lead exists
    lead = db.query(Lead).filter(Lead.id == interaction_update.lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Update fields
    update_data = interaction_update.model_dump()
    for field, value in update_data.items():
        setattr(db_interaction, field, value)
    
    db.commit()
    db.refresh(db_interaction)
    return db_interaction

@router.delete("/{interaction_id}", status_code=204)
def delete_interaction(interaction_id: int, db: Session = Depends(get_db)):
    """Delete an interaction"""
    db_interaction = db.query(Interaction).filter(Interaction.id == interaction_id).first()
    if not db_interaction:
        raise HTTPException(status_code=404, detail="Interaction not found")
    
    db.delete(db_interaction)
    db.commit()
    return None