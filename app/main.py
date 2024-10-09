import logging
import logging.config
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.products.routers import category_routes
from app.users.routers import user_routes

logging.basicConfig(level=logging.DEBUG)
config_path = os.path.join(os.path.dirname(__file__), "logging.conf")

logging.config.fileConfig(config_path, disable_existing_loggers=False)

# logging.config.fileConfig("logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("app")
logger.debug("Starting the application")


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(category_routes.router, prefix="/api/category", tags=["Category"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
