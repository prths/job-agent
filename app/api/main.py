import os
import uvicorn
from app.api.app import app

if not os.environ.get("GOOGLE_API_KEY"):
    raise RuntimeError("GOOGLE_API_KEY not set in environment")

if __name__ == "__main__":
    uvicorn.run(
        "app.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )
