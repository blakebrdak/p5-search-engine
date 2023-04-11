"""Search Server Configuration."""

import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# File Upload to var/uploads/
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent

DATABASE_FILENAME = PROJECT_ROOT/'var'/'search.sqlite3'
