from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import extract, and_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Legislation, LegislationType, Status

api_router = APIRouter()

@api_router.get("/federal")
async def get_federal_legislation(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    year: Optional[int] = None,
    congress: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Legislation).filter(
        Legislation.type == LegislationType.FEDERAL.value
    )

    # Apply filters
    if status:
        query = query.filter(Legislation.status == status)
    if year:
        query = query.filter(extract('year', Legislation.introduced_date) == year)
    if congress:
        query = query.filter(
            Legislation.extra_data['congress'].astext == str(congress)
        )

    # Get total count for pagination
    total = query.count()
    
    # Add sorting and pagination
    query = query.order_by(Legislation.introduced_date.desc())
    items = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "limit": limit,
        "data": items
    }

@api_router.get("/executive")
async def get_executive_orders(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    status: Optional[str] = None,
    year: Optional[int] = None,
    president: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Legislation).filter(
        Legislation.type == LegislationType.EXECUTIVE.value
    )

    # Apply filters
    if status:
        query = query.filter(Legislation.status == status)
    if year:
        query = query.filter(extract('year', Legislation.introduced_date) == year)
    if president:
        query = query.filter(
            Legislation.extra_data['president'].astext == president
        )

    # Get total count for pagination
    total = query.count()
    
    # Add sorting and pagination
    query = query.order_by(Legislation.introduced_date.desc())
    items = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "pages": (total + limit - 1) // limit,
        "limit": limit,
        "data": items
    }

@api_router.get("/legislation/{legislation_id}")
async def get_legislation_by_id(
    legislation_id: str,
    db: Session = Depends(get_db)
):
    item = db.query(Legislation).filter(
        Legislation.id == legislation_id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Legislation not found")
    
    return item

@api_router.get("/stats")
async def get_statistics(
    db: Session = Depends(get_db)
):
    federal_count = db.query(Legislation).filter(
        Legislation.type == LegislationType.FEDERAL.value
    ).count()
    
    executive_count = db.query(Legislation).filter(
        Legislation.type == LegislationType.EXECUTIVE.value
    ).count()
    
    state_count = db.query(Legislation).filter(
        Legislation.type == LegislationType.STATE.value
    ).count()
    
    return {
        "federal_count": federal_count,
        "executive_count": executive_count,
        "state_count": state_count
    }
