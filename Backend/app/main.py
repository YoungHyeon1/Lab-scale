from fastapi import FastAPI
from app.api.main import api_router
from app.core.config import settings
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware
from app.core.middle_ware import LogRequestsMiddleware


def custom_generate_unique_id(route: APIRoute) -> str:
    tag = route.tags[0] if route.tags else "default"
    return f"{tag}-{route.name}"

app = FastAPI(
    title='LOL API',
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
)

@app.get("/health")
async def health_check():
    """"
    Application LoadBlancer Health Chek
    """
    return JSONResponse(content={"status": "ok"}, status_code=200)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(LogRequestsMiddleware)
app.include_router(api_router, prefix=settings.API_V1_STR)
