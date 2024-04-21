from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables from .env file
load_dotenv()

# Import router containing API routes
from routes.route import router

# Create FastAPI instance
app = FastAPI()

# Include router in the application
app.include_router(router)
