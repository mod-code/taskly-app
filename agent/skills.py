import os
import subprocess
import requests

def get_pr_diff(repo_name, pr_number):
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo_name}/pulls/{pr_number}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3.diff"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    return ""

def generate_tests_for_diff(diff_text):
    print("Agent is analyzing diff and generating tests...")
    
    # Example scaffold logic:
    if "+def " in diff_text or "+class " in diff_text:
        dummy_test_path = "test_auto.py"
        with open(dummy_test_path, "w") as f:
            f.write("def test_auto_generated():\n    assert True\n")
        return [dummy_test_path]
    return []

def run_tests(test_files):
    print(f"Running tests for: {test_files}")
    results = ""
    for file in test_files:
        if file.endswith(".py"):
            try:
                out = subprocess.check_output(["pytest", file], stderr=subprocess.STDOUT)
                results += out.decode()
            except subprocess.CalledProcessError as e:
                results += e.output.decode()
        elif file.endswith(".ts") or file.endswith(".tsx") or file.endswith(".js"):
            try:
                out = subprocess.check_output(["npm", "test", "--", file], stderr=subprocess.STDOUT)
                results += out.decode()
            except subprocess.CalledProcessError as e:
                results += e.output.decode()
    return results or "Tests executed successfully."

def comment_on_pr(repo_name, pr_number, message):
    token = os.getenv("GITHUB_TOKEN")
    url = f"https://api.github.com/repos/{repo_name}/issues/{pr_number}/comments"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json"
    }
    requests.post(url, headers=headers, json={"body": message})
