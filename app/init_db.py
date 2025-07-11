from app.database import engine, Base
from app.models import admins, users, creators, not_interested, feedbacks

Base.metadata.create_all(bind=engine)
print("Database tables created.")
