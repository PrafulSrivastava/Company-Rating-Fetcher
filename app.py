from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from scraper import gather_all_ratings

app = FastAPI()

origins = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "chrome-extension://",
    "chrome-extension://*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "chrome-extension://*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ratings")
def get_ratings(company: str = Query(...), location: Optional[str] = Query(None)):
    results = gather_all_ratings(company, location)
    return {
        "company": company,
        "location": location,
        "ratings": results
    }
