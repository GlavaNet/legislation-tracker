from fastapi import APIRouter
from .base_routes import BaseRouter
from ..models.models import LegislationType

# Create router instances for each legislation type
api_router = APIRouter()

federal_router = BaseRouter(LegislationType.FEDERAL)
state_router = BaseRouter(LegislationType.STATE)
executive_router = BaseRouter(LegislationType.EXECUTIVE)

# Include routers with their prefixes
api_router.include_router(
    federal_router.router,
    prefix="/federal",
    tags=["federal"]
)

api_router.include_router(
    state_router.router,
    prefix="/state",
    tags=["state"]
)

api_router.include_router(
    executive_router.router,
    prefix="/executive",
    tags=["executive"]
)

# Add search endpoint
@api_router.get("/search/")
async def search_legislation(
    q: str,
    type: Optional[LegislationType] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Legislation)
    
    if type:
        query = query.filter(Legislation.type == type)
    
    results = query.filter(
        Legislation.title.ilike(f"%{q}%") |
        Legislation.summary.ilike(f"%{q}%")
    ).all()
    
    return results
