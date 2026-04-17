from fastapi import FastAPI
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware

logger.add("requests.log", level="INFO")

app = FastAPI()


origins = [
    "http://localhost:8000",
    "https://mysite.com",
    "null"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["Content-Type"],
)

@app.get("/greet/{username}")
async def greeting(username):
    logger.info(f"Received GET request to /greet/{username}")
    log_user_greeting(username)
    return {"greeting": f"Hello, {username}!"}

def log_user_greeting(username:str):
    logger.debug(f"Greeted user: {username}")





