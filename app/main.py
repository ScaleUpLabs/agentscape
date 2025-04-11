from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from api.routes.agents import router as agents_router
from db.database import init_db
from core.config import settings
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Create a limiter instance with a function to get the client's IP address
limiter = Limiter(key_func=get_remote_address)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database when the application starts
    init_db()
    yield
    # Cleanup operations can go here (if any)

app = FastAPI(
    title=settings.api_title,
    description=settings.api_description,
    lifespan=lifespan
)

# Add the limiter as a dependency to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Include the router with rate limiting
app.include_router(agents_router, prefix="/agents", tags=["agents"])