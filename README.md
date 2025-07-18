# Company Rating Fetcher

This project fetches company ratings from multiple sources (Trustpilot, Glassdoor, etc.) using web scraping. It provides an API endpoint to retrieve ratings for a given company and location.

## Setup

1. **Create and activate a virtual environment:**
   ```sh
   python -m venv .venv
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

3. **Install ChromeDriver:**
   - Download the version of ChromeDriver that matches your Chrome browser from: https://sites.google.com/chromium.org/driver/
   - Place the executable in your PATH or set the environment variable `CHROMEDRIVER_PATH` to its location.

   Example (Windows):
   ```sh
   $env:CHROMEDRIVER_PATH="C:\\path\\to\\chromedriver.exe"
   ```
   Example (macOS/Linux):
   ```sh
   export CHROMEDRIVER_PATH="/path/to/chromedriver"
   ```

## How to Run

Start the FastAPI app using Uvicorn:

```sh
uvicorn app:app --reload
```

## Example Usage

Request ratings for a company and location:

```sh
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"company": "google", "location": "Mountain View, CA"}' \
  http://localhost:8000/ratings
```
