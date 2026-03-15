import subprocess
import time
import os


def run_test(test_name):

    start_time = time.time()

    test_path = os.path.join("TestCases", test_name)

    process = subprocess.run(
        ["python", "-m", "pytest", test_path, "-s", "-v"],
        capture_output=True,
        text=True
    )

    execution_time = round(time.time() - start_time, 2)

    status = "PASS" if process.returncode == 0 else "FAIL"

    return {
        "test_name": test_name,
        "status": status,
        "execution_time": f"{execution_time}s",
        "stdout": process.stdout,
        "stderr": process.stderr
    }