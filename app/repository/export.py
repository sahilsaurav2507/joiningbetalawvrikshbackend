from app.utils.excel_export import export_to_excel
from app.models.users import User
from app.models.creators import Creator
from sqlalchemy.orm import Session

def export_table_to_excel(db: Session, table: str) -> str:
    if table == "users":
        rows = [u.__dict__ for u in db.query(User).all()]
    elif table == "creators":
        rows = [c.__dict__ for c in db.query(Creator).all()]
    else:
        raise ValueError("Invalid table name")
    filename = f"{table}_export.xlsx"
    export_to_excel(rows, filename)
    return filename 