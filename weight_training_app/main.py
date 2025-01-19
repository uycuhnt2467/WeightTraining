import uvicorn
from fastapi import FastAPI

app = FastAPI(
    title="Weight Training API",
    description="API for tracking weight training progress",
    version="0.1.0",
    docs_url="/docs",  # Swagger UI endpoint (default)
    redoc_url="/redoc",  # ReDoc endpoint (alternative docs, default)
    openapi_url="/openapi.json"  # OpenAPI schema endpoint (default)
)

@app.get("/")
def read_root():
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
    uvicorn.run("weight_training_app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_server()
