import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.api import router as api_router
from core.config import (
    ALLOWED_HOSTS,
    API_V1_PREFIX,
    SERVICE_NAME,
    SERVICE_VERSION,
)
from db.sqlite_utils import create_db_and_tables

log = logging.getLogger("uvicorn.error")

service_description = """
This can be your first step towards large production ideas. 🚀🚀🚀 <br/>
We can use the project structure and evaluate further according to the needs.
"""

app = FastAPI(
    title=SERVICE_NAME,
    description=service_description,
    version=SERVICE_VERSION,
    terms_of_service="https://company.com/terms",
    contact={
        "name": "Company Name",
        "url": "https://company.com",
        "email": "contact@company.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # openapi_tags=api_tags_metadata,
    openapi_url=f"{API_V1_PREFIX}/openapi.json",  # openapi.json
    docs_url=f"{API_V1_PREFIX}/docs/",  # Swagger
    redoc_url=f"{API_V1_PREFIX}/redoc/",  # Redoc
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(ALLOWED_HOSTS),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
    prefix=API_V1_PREFIX,
)


@app.on_event("startup")
async def startup_event():
    log.info("Startup event initiate")
    create_db_and_tables()
    log.info("Startup event completed")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutdown event initiate")
    # Do something...
    log.info("Shutdown event completed")
