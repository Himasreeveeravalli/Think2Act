import sys
import os
from pathlib import Path

# Add project directory to python path
project_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(project_dir))

from app import app

if __name__ == "__main__":
    print("=================================================================")
    print(" Starting AI Multi-Agent E-Commerce Shopping Assistant Studio")
    print(" Server running at: http://127.0.0.1:5000")
    print("=================================================================")
    app.run(host="127.0.0.1", port=5000, debug=False)
