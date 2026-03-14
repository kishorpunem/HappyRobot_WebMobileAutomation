from fastapi import FastAPI
from api.routes.automation_routes import router as automation_router
from api.routes.health_routes import router as health_router

app = FastAPI(title="HappyRobot Automation API")

app.include_router(health_router)
app.include_router(automation_router)