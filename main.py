from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import leads, interactions, reports

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mini CRM System",
    description="A simple CRM system to manage customer leads and interactions",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router, prefix="/leads", tags=["Leads"])
app.include_router(interactions.router, prefix="/interactions", tags=["Interactions"])
app.include_router(reports.router, prefix="/reports", tags=["Reports"])

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Mini CRM System",
        "endpoints": {
            "leads": "/leads",
            "interactions": "/interactions",
            "reports": "/reports",
            "docs": "/docs"
        }
    }