from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.routes import router
from app.db.database import init_db
import traceback

app = FastAPI(
    title="Job Application Agent",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": str(exc),
            "trace": traceback.format_exc()
        },
    )

app.include_router(router)
