from fastapi import APIRouter
from api.schemas.automation_schema import run_test

router = APIRouter(prefix="/automation", tags=["Automation"])

@router.post("/run-test")
def run_automation(test_name: str):

    result = run_test(test_name)

    return {
        "message": "Automation executed",
        "result": result
    }