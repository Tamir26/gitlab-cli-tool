# GitLab Role Manager and Activity Fetcher

This project provides a command-line tool for managing GitLab user roles and listing merge requests or issues created in a specific year. It supports both local and Dockerized usage.

## Features

- 🔑 Assign or update a user's role in a GitLab **project or group**
- 📅 List **issues** or **merge requests** created in a given **year**
- 🐳 Run as a Docker container with environment variables

---

## Requirements

- Python 3.11+
- GitLab Personal Access Token
- Docker (optional, for containerized use)

---

## Environment Variables

| Variable      | Description                  |
|---------------|------------------------------|
| `GITLAB_URL`  | Base URL of your GitLab instance (e.g. `https://gitlab.com`) |
| `GITLAB_TOKEN`| Personal access token with required API scopes (e.g. `read_api`, `api`) |

---

## Installation

### 🔧 Local Setup (Python)

```bash
# Clone this repo
git clone https://github.com/your-user/mobilye-assignment.git
cd mobilye-assignment

# Install dependencies
pip install -r requirements.txt

# Export required environment variables
export GITLAB_URL=https://gitlab.com
export GITLAB_TOKEN=your_token
