# SOLUTION.md

## Technical Decisions and Rationale
- **Agent Environment**: The agent is implemented in Python using the standard `requests` and `openai` libraries for orchestrating the workflow. Python is chosen for its rich ecosystem in AI/ML, ease of integration, and simplicity in scripting.
- **Workflow Automation**: GitHub Actions is used to trigger the agent automatically whenever a Pull Request is opened or updated. It provides a seamless, secure CI/CD environment with direct access to PR contexts.
- **Agent Skills**: The agent is built with distinct, reusable tools/skills (located in `agent/skills.py`):
  - `get_pr_diff`: Analyzes the PR diff to understand changes.
  - `generate_tests_for_diff`: Generates or updates frontend (Jest/React) and backend (Pytest/FastAPI) tests using LLM inference.
  - `run_tests`: Executes the tests in an isolated step to verify correctness.
  - `comment_on_pr`: Publishes the results back to the PR.

## Prerequisites & Running the Workflow
1. Add `OPENAI_API_KEY` to your GitHub Repository Secrets.
2. Ensure the GitHub Actions worker has `write` permissions for Pull Requests (Settings -> Actions -> General -> Workflow permissions).
3. The workflow (`.github/workflows/agent_pr.yml`) runs automatically on new or updated PRs.

## Agent and Skills Definition
- **Location**: The agent code resides in the `agent/` directory.
- **Usage**: `agent/main.py` orchestrates the workflow. Reusable skills are defined in `agent/skills.py` as Python functions that act as discrete tools.

## Example Run Scenario
1. A developer opens a PR adding a `UserRegistration` component.
2. The GitHub Action triggers `agent/main.py`.
3. The agent fetches the diff and notices new React code without corresponding `.test.tsx` files.
4. It calls the test generator skill to write `UserRegistration.test.tsx` locally.
5. It uses the test runner skill to execute `npm test` on the new file.
6. Based on the successful run, it posts a comment on the PR with the test output and details of the generated code.

## Assumptions
- Code is reasonably modular so that unit tests can be written without excessive mocking.
- The environment has `npm` and `pytest` configured correctly in the base repository.

## Limitations
- **Context Window**: Extremely large PRs might exceed the LLM's context limit.
- **Hallucinations**: The LLM might generate tests that use mocked dependencies incorrectly.

## Future Improvements
- Implement an iterative retry mechanism (if a generated test fails, feed the error back to the LLM to fix it).
- Add functionality to automatically commit and push the generated tests back to the branch.
