from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from ..models import Legislation, LegislationType

api_router = APIRouter()

@api_router.get("/federal")  # Note: removed trailing slash
async def get_federal_legislation(
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Legislation).filter(
        Legislation.type == LegislationType.FEDERAL
    )
    total = query.count()
    legislations = query.offset((page - 1) * limit).limit(limit).all()
    
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": legislations
    }

@api_router.get("/health")
async def health_check():
    return {"status": "healthy"}
