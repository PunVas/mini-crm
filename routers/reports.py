from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models import Lead, Interaction

router = APIRouter()

@router.get("/leads-by-status")
def get_leads_by_status(db: Session = Depends(get_db)):
    """Get count of leads grouped by status"""
    results = db.query(
        Lead.status, 
        func.count(Lead.id).label("count")
    ).group_by(Lead.status).all()
    
    return {
        "total_leads": sum(r.count for r in results),
        "by_status": {r.status: r.count for r in results}
    }

@router.get("/interactions-summary")
def get_interactions_summary(db: Session = Depends(get_db)):
    """Get count of interactions grouped by type"""
    results = db.query(
        Interaction.interaction_type,
        func.count(Interaction.id).label("count")
    ).group_by(Interaction.interaction_type).all()
    
    return {
        "total_interactions": sum(r.count for r in results),
        "by_type": {r.interaction_type: r.count for r in results}
    }

@router.get("/dashboard")
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Get comprehensive dashboard data"""
    # Lead statistics
    total_leads = db.query(func.count(Lead.id)).scalar()
    lead_status = db.query(
        Lead.status, 
        func.count(Lead.id).label("count")
    ).group_by(Lead.status).all()
    
    # Interaction statistics
    total_interactions = db.query(func.count(Interaction.id)).scalar()
    interaction_types = db.query(
        Interaction.interaction_type,
        func.count(Interaction.id).label("count")
    ).group_by(Interaction.interaction_type).all()
    
    # Top companies by lead count
    top_companies = db.query(
        Lead.company,
        func.count(Lead.id).label("lead_count")
    ).group_by(Lead.company).order_by(func.count(Lead.id).desc()).limit(5).all()
    
    return {
        "leads": {
            "total": total_leads,
            "by_status": {r.status: r.count for r in lead_status}
        },
        "interactions": {
            "total": total_interactions,
            "by_type": {r.interaction_type: r.count for r in interaction_types}
        },
        "top_companies": [
            {"company": c.company, "lead_count": c.lead_count} 
            for c in top_companies
        ]
    }