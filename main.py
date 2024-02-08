from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import ResponseValidationError

from app.api.v1.endpoints import event, user
from app.db.database import Base, engine


Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(user.router, prefix="/api/v1/users", tags=["user"])
app.include_router(event.router, prefix="/api/v1/events", tags=["event"])


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request, exc):
    error = str(exc)
    return JSONResponse(status_code=400, content={"message": error})