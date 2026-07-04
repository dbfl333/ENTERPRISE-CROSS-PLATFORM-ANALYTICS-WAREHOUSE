# Skill 1: Operating System Workspace Provisioning & Environment Setup

## Objective
Autonomously verify, install, and instantiate the development environment on Windows hardware.

## Verification Checklist
1. **Git & Git Bash:** Check if Git is installed (`git --version`).
2. **Terminal Routing:** Verify Git Bash availability or standard shell access.
3. **Python & Package Manager:** Check if Python is installed and accessible.

## Setup Sequence
1. **Provision Git (If Missing):**
   ```dos
   winget install Git.Git --silent --accept-source-agreements --accept-package-agreements
   ```
2. **Initialize Local Git Repository:**
   ```bash
   git init
   ```
3. **Configure Project Exclusions (.gitignore):**
   Create a root `.gitignore` containing:
   ```text
   # Local Environment Variables
   .env
   
   # Python Cache Directories
   __pycache__/
   *.pyc
   *.pyo
   *.pyd
   .venv/
   venv/
   
   # Compiled Storage & DB Binaries
   *.duckdb
   *.db
   
   # IDE Settings
   .vscode/
   .idea/
   ```

4. **Directory Structure Construction:**
   Construct the following 5-tier architecture:
   ```text
   ENTERPRISE-CROSS-PLATFORM-ANALYTICS-WAREHOUSE/
   ├── .agents/
   │   ├── workflows/
   │   └── skills/
   ├── 01_data_generation/
   ├── 02_raw_data/
   ├── 03_etl_pipelines/
   ├── 04_clean_data/
   └── 05_dashboard/
       └── pages/
   ```
