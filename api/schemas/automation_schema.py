import subprocess

def run_test(test_name):

    process = subprocess.run(
        ["python", "-m", "pytest", f"TestCases/{test_name}"],
        capture_output=True,
        text=True
    )

    return {
        "stdout": process.stdout,
        "stderr": process.stderr,
        "status": "PASS" if process.returncode == 0 else "FAIL"
    }