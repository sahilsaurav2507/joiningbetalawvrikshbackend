from fastapi import FastAPI
from app.middleware.cors import setup_cors
from app.routes import admin, user, creator, not_interested, feedback

app = FastAPI()

setup_cors(app)

# Import and include routers here
app.include_router(admin.router)
app.include_router(user.router)
app.include_router(creator.router)
app.include_router(not_interested.router)
app.include_router(feedback.router)

@app.get("/")
def root():
    return {"message": "Lawvriksh Backend Running"} 