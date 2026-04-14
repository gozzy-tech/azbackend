from fastapi import FastAPI
from app.core.config import settings
from app.core.routes import router as main_router
from app.core.middleware import register_middleware

description = """
REST API service demonstrating full deployment to Azure Cloud Infrastructure, housing my portfolio , courses and experiences.
"""

app = FastAPI(title=settings.SERVICE_NAME,
              description=description,
              version=settings.VERSION,
              contact={
                  "name": "",
                  "url": "https://gozzytech.com",
                  "email": "chiagoziendukwe@gmail.com",
              },
              )


version_prefix = "/api/v1"
app.include_router(main_router, prefix=version_prefix)

register_middleware(app)


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Azure Deployment API!"}
