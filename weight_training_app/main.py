import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from .routers import user, auth
from fastapi.middleware.cors import CORSMiddleware
import logging



logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
    format="%(asctime)s | %(levelname)-8s | "
            "%(module)s:%(funcName)s:%(lineno)d - %(message)s")


logger.info("test")
app = FastAPI(
    title="Weight Training API",
    description="API for tracking weight training progress",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI endpoint (default)
    redoc_url="/redoc",  # ReDoc endpoint (alternative docs, default)
    openapi_url="/openapi.json",  # OpenAPI schema endpoint (default)
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the security scheme that will appear in the OpenAPI docs
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@app.get("/")
def read_root():
    logger.info("GET / endpoint called!")
    return {"message": "Hello, World!"}

# Example route to test the API docs
@app.get("/hello", tags=["Test"])
async def hello_world():
    """
    Test endpoint that returns a greeting message.
    
    Returns:
        dict: A greeting message
    """
    return {"message": "Hello, Weight Training App!"}

def start_server():
    """Entry point for the application."""
    uvicorn.run("weight_training_app.main:app", host="0.0.0.0", port=8000, reload=True, log_level="debug")


app.include_router(user.router)
app.include_router(auth.router)

if __name__ == "__main__":
    start_server()
