from app.database import SessionLocal
from app.models import Legislation, LegislationType

def main():
    db = SessionLocal()
    try:
        federal_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.FEDERAL.value
        ).count()
        
        state_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.STATE.value
        ).count()
        
        exec_count = db.query(Legislation).filter(
            Legislation.type == LegislationType.EXECUTIVE.value
        ).count()
        
        print("\nDatabase Contents:")
        print(f"Federal Bills: {federal_count}")
        print(f"State Bills: {state_count}")
        print(f"Executive Orders: {exec_count}")
        
        for type_ in [LegislationType.FEDERAL.value, LegislationType.STATE.value, LegislationType.EXECUTIVE.value]:
            items = db.query(Legislation).filter(
                Legislation.type == type_
            ).limit(3).all()
            if items:
                print(f"\n{type_.title()} Items:")
                for item in items:
                    print(f"- {item.title[:100]}...")
    finally:
        db.close()

if __name__ == "__main__":
    main()
