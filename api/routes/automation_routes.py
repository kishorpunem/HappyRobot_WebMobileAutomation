# from fastapi import APIRouter
# from api.schemas.automation_schema import run_test
#
# router = APIRouter(prefix="/automation", tags=["Automation"])
#
# @router.post("/run-test/CreateInquiryforGCC")
# def run_automation(test_name: str):
#
#     result = run_test(test_name)
#
#     return {
#         "message": "Automation executed",
#         "result": result
#     }

from fastapi import APIRouter
from api.schemas.automation_schema import run_test
from api.save_execution import save_test_execution
from datetime import datetime

router = APIRouter(prefix="/automation", tags=["Automation"])

@router.post("/run-test/CreateInquiryforGCC")
def run_automation(test_name: str):

    result = run_test(test_name)

    # Prepare data for DB
    execution_data = {
        "test_name": test_name,
        "status": result.get("status"),
        "execution_time": result.get("execution_time"),
        "inquiry_no": result.get("inquiry_no"),
        "inquiry_movetype": result.get("inquiry_movetype"),
        "inquiry_creationdatetime": result.get("inquiry_creationdatetime")
    }

    # Save into database
    save_test_execution(execution_data)

    return {
        "message": "Automation executed",
        "result": result
    }