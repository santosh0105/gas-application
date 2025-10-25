from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api import auth, users, orders, cylinders
from app.models.models import Base
from app.db.session import engine

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.PROJECT_VERSION,
    description="Gas Cylinder Booking System API"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, tags=["authentication"])
app.include_router(users.router, prefix="/api", tags=["users"])
app.include_router(orders.router, prefix="/api", tags=["orders"])
app.include_router(cylinders.router, prefix="/api", tags=["cylinders"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to Gas Cylinder Booking System API",
        "documentation": "/docs",
        "redoc": "/redoc"
    }
