import os
import sys
import subprocess
import streamlit as st

# 1. Fetch credentials securely from Streamlit Secrets
token = st.secrets["GITHUB_TOKEN"]
username = st.secrets["GITHUB_USERNAME"]
repo_name = st.secrets["PRIVATE_REPO_NAME"]
target_script = st.secrets["PRIVATE_SCRIPT_NAME"] # e.g., "main_app.py"

# 2. Define local cloning destination
local_dir = "/tmp/private_repo"

# 3. Clone the private repository programmatically if it doesn't exist
if not os.path.exists(local_dir):
    clone_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    subprocess.run(["git", "clone", clone_url, local_dir], check=True)

# 4. Append the private directory to Python path to resolve imports
sys.path.append(local_dir)

# 5. Dynamically execute the private script
private_script_path = os.path.join(local_dir, target_script)
with open(private_script_path, "r") as f:
    code = f.read()
    
# Execute the private code within the current global context
exec(code, globals())