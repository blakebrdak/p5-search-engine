"""Search Server Configuration."""

import pathlib

SEARCH_INDEX_SEGMENT_API_URLS = [
    "http://localhost:9000/api/v1/hits/",
    "http://localhost:9001/api/v1/hits/",
    "http://localhost:9002/api/v1/hits/",
]

# File Upload to var/uploads/
SEARCH_ROOT = pathlib.Path(__file__).resolve().parent.parent

DATABASE_FILENAME = SEARCH_ROOT/'sql'/'search.sql'