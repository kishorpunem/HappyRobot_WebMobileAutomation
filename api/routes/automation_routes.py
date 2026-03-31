from fastapi import APIRouter
from api.schemas.automation_schema import run_test
from api.save_execution import save_test_execution
import re

router = APIRouter(prefix="/automation", tags=["Automation"])

@router.post("/run-test/CreateInquiryforGCC")
def run_automation(test_name: str):

    result = run_test(test_name)

    print("RESULT FROM TEST:", result)

    stdout = result.get("stdout", "")

    # Extract values from stdout using regex
    inquiry_no = None
    inquiry_movetype = None
    inquiry_creationdatetime = None

    inquiry_match = re.search(r"inquiry_no':\s*'([^']+)'", stdout)
    movetype_match = re.search(r"inquiry_movetype':\s*'([^']+)'", stdout)
    datetime_match = re.search(r"inquiry_creationdatetime':\s*'([^']+)'", stdout)

    if inquiry_match:
        inquiry_no = inquiry_match.group(1)

    if movetype_match:
        inquiry_movetype = movetype_match.group(1)

    if datetime_match:
        inquiry_creationdatetime = datetime_match.group(1)

    execution_data = {
        "test_name": result.get("test_name"),
        "status": result.get("status"),
        "execution_time": result.get("execution_time"),
        "inquiry_no": inquiry_no,
        "inquiry_movetype": inquiry_movetype,
        "inquiry_creationdatetime": inquiry_creationdatetime
    }

    print("DATA SENT TO DB:", execution_data)

    save_test_execution(execution_data)

    return {
        "message": "Automation executed",
        "result": result
    }