#!/bin/bash

cd backend
source venv/bin/activate

# Create a Python script to check database
cat > check_db.py << 'EOF'
from app.database import SessionLocal
from app.models import Legislation, LegislationType

def main():
    db = SessionLocal()
    try:
        federal_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.FEDERAL
        ).count()
        
        state_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.STATE
        ).count()
        
        executive_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.EXECUTIVE
        ).count()
        
        print("\nDatabase Contents:")
        print(f"Federal Bills: {federal_count}")
        print(f"State Bills: {state_count}")
        print(f"Executive Orders: {executive_count}")
        
        # Show some sample data
        print("\nSample Items:")
        for type_ in [LegislationType.FEDERAL, LegislationType.STATE, LegislationType.EXECUTIVE]:
            items = db.query(Legislation).filter(Legislation.type == type_).limit(3).all()
            if items:
                print(f"\n{type_.value.title()} Items:")
                for item in items:
                    print(f"- {item.title[:100]}...")
    finally:
        db.close()

if __name__ == "__main__":
    main()
EOF

python check_db.py
