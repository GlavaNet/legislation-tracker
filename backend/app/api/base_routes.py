from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from ..database import get_db
from ..models.models import Legislation, LegislationType
from datetime import datetime

class BaseRouter:
    def __init__(self, legislation_type: LegislationType):
        self.router = APIRouter()
        self.legislation_type = legislation_type
        self.setup_routes()

    def setup_routes(self):
        @self.router.get("/")
        async def get_legislation(
            page: int = Query(1, ge=1),
            limit: int = Query(20, ge=1, le=100),
            status: Optional[str] = None,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None,
            db: Session = Depends(get_db)
        ):
            query = db.query(Legislation).filter(
                Legislation.type == self.legislation_type
            )

            if status:
                query = query.filter(Legislation.status == status)
            if start_date:
                query = query.filter(Legislation.introduced_date >= start_date)
            if end_date:
                query = query.filter(Legislation.introduced_date <= end_date)

            total = query.count()
            items = query.offset((page - 1) * limit).limit(limit).all()
            
            return {
                "total": total,
                "page": page,
                "limit": limit,
                "data": items
            }

        @self.router.get("/{legislation_id}")
        async def get_legislation_by_id(
            legislation_id: str,
            db: Session = Depends(get_db)
        ):
            item = db.query(Legislation).filter(
                Legislation.id == legislation_id,
                Legislation.type == self.legislation_type
            ).first()
            
            if not item:
                raise HTTPException(status_code=404, detail="Legislation not found")
            return item
