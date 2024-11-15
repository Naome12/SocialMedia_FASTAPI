import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from app.models.Users import Base  # Ensure this is correctly imported from your models

# Load environment variables from .env file
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the sync engine for SQLAlchemy (replacing AsyncEngine)
engine = create_engine(DATABASE_URL, echo=True)

# Create a sessionmaker with the sync session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to initialize the database (creating tables etc.)
def init_db():
    import app.models.Users
    import app.models.Posts
    Base.metadata.create_all(bind=engine)
