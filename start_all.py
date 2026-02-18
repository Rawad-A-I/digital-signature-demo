import subprocess
import time
import os
import sys

# Define services with their ports and module paths
services = [
    # Level 1
    {"name": "L1-Receiver", "module": "receiver.Level1.app:app", "port": 8021},
    {"name": "L1-Sender", "module": "sender.Level1.app:app", "port": 8022},
    # Level 2
    {"name": "L2-Receiver", "module": "receiver.Level2.app:app", "port": 8011},
    {"name": "L2-Sender", "module": "sender.Level2.app:app", "port": 8012},
    # Level 3
    {"name": "L3-Receiver", "module": "receiver.Level3.app:app", "port": 8001},
    {"name": "L3-Sender", "module": "sender.Level3.app:app", "port": 8002},
]

# Path to python in venv
if sys.platform == "win32":
    python_exe = os.path.join("venv", "Scripts", "python.exe")
else:
    python_exe = os.path.join("venv", "bin", "python")

uvicorn_exe = os.path.join(os.path.dirname(python_exe), "uvicorn")

processes = []

try:
    print("--- Starting Backend Services ---")
    for svc in services:
        print(f"Starting {svc['name']} on port {svc['port']}...")
        proc = subprocess.Popen(
            [uvicorn_exe, svc['module'], "--port", str(svc['port']), "--host", "127.0.0.1"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        processes.append(proc)
        time.sleep(1)

    print("\n--- Starting Frontend Server ---")
    print("Starting Frontend on http://localhost:8000...")
    frontend_proc = subprocess.Popen(
        [python_exe, "-m", "http.server", "8000", "--bind", "127.0.0.1"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    processes.append(frontend_proc)

    print("\nAll systems online!")
    print("Frontend URL: http://localhost:8000")
    print("\nPress Ctrl+C to stop all servers.")

    # Keep the script running
    while True:
        time.sleep(1)

except KeyboardInterrupt:
    print("\nShutting down servers...")
    for proc in processes:
        proc.terminate()
    print("Stopped.")
except Exception as e:
    print(f"\nError: {e}")
    for proc in processes:
        proc.terminate()
