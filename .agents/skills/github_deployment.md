# Skill 5: Public Repository Creation & Deployment

## Objective
Establish a clean version control pipeline, create a public repository on the user's GitHub account using the GitHub CLI (`gh`), link the workspace, and push the verified infrastructure codebase safely.

## Deployment Steps
1. **GitHub CLI Installation & Verification:**
   Ensure `gh` is installed (`winget install GitHub.cli`). Check authentication status:
   ```bash
   gh auth status
   ```
2. **Repository Creation:**
   Create a public repository with the exact workspace name:
   ```bash
   gh repo create ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE --public --description "Centralized enterprise data warehouse and business intelligence pipeline integrating multi-tenant microservice telemetry using DuckDB and Streamlit."
   ```
3. **Repository Linking:**
   Set the origin URL to link local Git with GitHub:
   ```bash
   git remote add origin https://github.com/<user_account_name>/ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE.git
   ```
4. **Ignored Files Check:**
   Verify that sensitive folders and databases are not tracked by staging files:
   ```bash
   git status
   ```
5. **Stage, Commit & Push:**
   Execute standard tracking sequence:
   ```bash
   git add .
   git commit -m "Infrastructure Buildout: Established cross-platform schema boundaries, agent operational skill layers, and git staging rules."
   git branch -M main
   git push -u origin main
   ```
