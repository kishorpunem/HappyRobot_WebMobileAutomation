from fastapi import FastAPI
import subprocess

app = FastAPI()

@app.get("/")
def home():
    return {"message": "HappyRobot Automation API Running"}

@app.post("/create-inquiry")
def create_inquiry():

    process = subprocess.run(
        ["python", "-m", "pytest", "TestCases/test_TC001_AInquiryCreationUAECB.py"],
        capture_output=True,
        text=True
    )

    return {
        "status": "Automation executed",
        "output": process.stdout,
        "error": process.stderr
    }