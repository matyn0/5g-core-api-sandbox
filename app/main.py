from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_tables
from app.routers import nef, nwdaf


# FastAPI runs the code before yield when the application starts.
# Code placed after yield would run when the application shuts down.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables if they do not already exist.
    # Existing tables and stored subscriptions remain untouched.
    create_tables()

    # Hand control back to FastAPI so it can serve requests.
    yield


app = FastAPI(
    title="5G Core API Sandbox",
    description="Sandbox for simulating 5G NEF and NWDAF APIs.",
    version="0.1.0",
    lifespan=lifespan,
)

@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(nef.router)
app.include_router(nwdaf.router)
