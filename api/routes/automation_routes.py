import os
import subprocess
import time
from fastapi import APIRouter, WebSocket

router = APIRouter()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
TEST_FOLDER = os.path.join(BASE_DIR, "TestCases")
# TEST_FOLDER = os.path.join(os.getcwd(), "TestCases")

execution_history = []

connected_clients = []

# -----------------------------
# GET TEST CASES
# -----------------------------
@router.get("/automation/get-tests")
def get_tests():

    tests = []

    for file in os.listdir(TEST_FOLDER):

        if file.startswith("test_") and file.endswith(".py"):

            tests.append({
                "name": file,
                "status": "Not Run",
                "duration": "-",
                "last_run": "-"
            })

    return {"tests": tests}


# -----------------------------
# RUN SINGLE TEST
# -----------------------------
@router.post("/automation/run-test/{name}")
def run_test(name: str):

    start = time.time()

    result = subprocess.run(
        ["pytest", f"{TEST_FOLDER}/{name}"],
        capture_output=True,
        text=True
    )

    duration = round(time.time() - start, 2)

    status = "PASS" if result.returncode == 0 else "FAIL"

    execution_history.append({
        "test": name,
        "status": status,
        "duration": duration,
        "time": time.strftime("%H:%M:%S")
    })

    return {
        "result": {
            "status": status,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    }


# -----------------------------
# RUN ALL TESTS
# -----------------------------
@router.post("/automation/run-all-tests")
def run_all_tests():

    result = subprocess.run(
        ["pytest", TEST_FOLDER],
        capture_output=True,
        text=True
    )

    return {"stdout": result.stdout}


# -----------------------------
# EXECUTION HISTORY
# -----------------------------
@router.get("/automation/history")
def history():

    return {"history": execution_history}


# -----------------------------
# SELENIUM GRID STATUS
# -----------------------------
@router.get("/automation/grid-status")
def grid_status():

    return {
        "nodes": [
            {"id": 1, "status": "Idle"},
            {"id": 2, "status": "Running"},
            {"id": 3, "status": "Idle"},
            {"id": 4, "status": "Idle"}
        ]
    }


# -----------------------------
# REAL TIME LOG STREAM
# -----------------------------
@router.websocket("/automation/log-stream")
async def log_stream(websocket: WebSocket):

    await websocket.accept()

    connected_clients.append(websocket)

    while True:
        await websocket.receive_text()