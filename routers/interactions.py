from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Lead
from schemas import LeadCreate, LeadUpdate, Lead as LeadSchema, LeadWithInteractions

router = APIRouter()

@router.post("/", response_model=LeadSchema, status_code=201)
def create_lead(lead: LeadCreate, db: Session = Depends(get_db)):
    """Create a new lead"""
    # Check if email already exists
    existing_lead = db.query(Lead).filter(Lead.email == lead.email).first()
    if existing_lead:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    db_lead = Lead(**lead.model_dump())
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.get("/", response_model=List[LeadSchema])
def get_leads(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    name: Optional[str] = None,
    status: Optional[str] = None,
    company: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get all leads with optional filters"""
    query = db.query(Lead)
    
    if name:
        query = query.filter(Lead.name.ilike(f"%{name}%"))
    if status:
        query = query.filter(Lead.status == status)
    if company:
        query = query.filter(Lead.company.ilike(f"%{company}%"))
    
    leads = query.offset(skip).limit(limit).all()
    return leads

@router.get("/{lead_id}", response_model=LeadWithInteractions)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """Get a specific lead by ID with interactions"""
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead

@router.put("/{lead_id}", response_model=LeadSchema)
def update_lead(lead_id: int, lead_update: LeadUpdate, db: Session = Depends(get_db)):
    """Update a lead"""
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    # Check if email is being updated and already exists
    if lead_update.email and lead_update.email != db_lead.email:
        existing = db.query(Lead).filter(Lead.email == lead_update.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    update_data = lead_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_lead, field, value)
    
    db.commit()
    db.refresh(db_lead)
    return db_lead

@router.delete("/{lead_id}", status_code=204)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    """Delete a lead"""
    db_lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not db_lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    
    db.delete(db_lead)
    db.commit()
    return None