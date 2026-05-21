import os
import sys
import subprocess
import streamlit as st

# Retrieve secrets
token = st.secrets["GITHUB_TOKEN"]
username = st.secrets["GITHUB_USERNAME"]
repo_name = st.secrets["PRIVATE_REPO_NAME"]
target_script = st.secrets["PRIVATE_SCRIPT_NAME"]

local_dir = "/tmp/private_repo"

# Robust cloning logic with error tracking
if not os.path.exists(local_dir):
    clone_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    
    # Capture stderr to catch authentication or repository path errors
    result = subprocess.run(["git", "clone", clone_url, local_dir], capture_output=True, text=True)
    
    if result.returncode != 0:
        st.error("### ❌ Git Clone Failed")
        st.code(result.stderr, language="bash")
        st.stop()

# Execution context
sys.path.append(local_dir)
private_script_path = os.path.join(local_dir, target_script)

if not os.path.exists(private_script_path):
    st.error(f"### ❌ File Not Found inside Container")
    st.write(f"Expected path: `{private_script_path}`")
    st.write("Available files in directory:")
    st.code(os.listdir(local_dir))
    st.stop()

with open(private_script_path, "r") as f:
    code = f.read()

exec(code, globals())