from fastapi import FastAPI
from app.adapter.mendeley.token_provider import new_mendeley_token_provider
from app.handler.v1.router import v1_router


app = FastAPI()


@app.get("/health")
async def health_check():
    return {"status": "ok"}


app.include_router(v1_router, prefix="/v1")
