import os
import sys
from skills import get_pr_diff, generate_tests_for_diff, run_tests, comment_on_pr

def main():
    repo = os.getenv("REPO_NAME")
    pr_number = os.getenv("PR_NUMBER")
    
    if not repo or not pr_number:
        print("Missing GitHub PR context. Ensure REPO_NAME and PR_NUMBER are set.")
        sys.exit(1)
        
    print(f"Starting agent analysis for {repo} PR #{pr_number}")
    
    # Skill 1: Read Diff
    diff = get_pr_diff(repo, pr_number)
    if not diff:
        print("No changes found or failed to fetch diff.")
        sys.exit(0)
        
    # Skill 2: Generate Tests
    generated_files = generate_tests_for_diff(diff)
    
    if not generated_files:
        comment_on_pr(repo, pr_number, "🤖 **Agent Analysis:** No missing unit tests identified for these changes.")
        sys.exit(0)
        
    # Skill 3: Run Tests
    test_results = run_tests(generated_files)
    
    # Skill 4: Report Results
    report = f"### 🤖 Agentic Test Generation Results\n\n"
    report += "The agent generated/updated the following tests based on the PR diff:\n"
    for file in generated_files:
        report += f"- `{file}`\n"
    report += f"\n#### Test Execution Output:\n```\n{test_results}\n```"
    
    comment_on_pr(repo, pr_number, report)
    print("Agent workflow completed.")

if __name__ == "__main__":
    main()
