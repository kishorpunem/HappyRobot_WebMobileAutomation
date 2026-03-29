from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes.automation_routes import router as automation_router
from api.routes.health_routes import router as health_router

app = FastAPI(title="HappyRobot Automation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow frontend requests
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(automation_router)