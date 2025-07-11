from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.database import SessionLocal
from app.models.admins import Admin
from app.utils.jwt_handler import create_access_token, verify_access_token
from app.utils.password import verify_password
from app.schemas.admins import AdminOut
from app.repository.admin import get_admin_by_email
from app.repository.users import get_all_users
from app.repository.creators import get_all_creators
from app.repository.export import export_table_to_excel
from app.config import settings
from fastapi.responses import FileResponse

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/adminlogin")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/adminlogin")
def admin_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = get_admin_by_email(db, form_data.username)
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": admin.email})
    return {"access_token": token, "token_type": "bearer"}


def get_current_admin(token: str = Depends(oauth2_scheme)):
    payload = verify_access_token(token)
    if not payload or payload.get("sub") != settings.ADMIN_EMAIL:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload

@router.get("/registereduserdata", response_model=list[dict])
def get_registered_users(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return get_all_users(db)

@router.get("/registeredcreatordata", response_model=list[dict])
def get_registered_creators(db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    return get_all_creators(db)

@router.post("/downloaddata")
def download_data(table: str, db: Session = Depends(get_db), admin=Depends(get_current_admin)):
    filename = export_table_to_excel(db, table)
    return FileResponse(filename, media_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', filename=filename) 