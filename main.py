from dotenv import load_dotenv
from fastapi import FastAPI

load_dotenv()

from routes.route import router

app = FastAPI()

app.include_router(router)




