from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from api.routes.automation_routes import router as automation_router
from api.routes.health_routes import router as health_router

app = FastAPI(title="HappyRobot Automation API")

# Templates folder
templates = Jinja2Templates(directory="templates")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(automation_router)

# Dashboard UI
@app.get("/")
def dashboard():
    return FileResponse("UICode/index.html")