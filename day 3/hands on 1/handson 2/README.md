# Handson 2 ETL App

Minimal FastAPI app demonstrating a second ETL example.

- `POST /upload` returns cleaned CSV file download
- `POST /upload/json` returns cleaned JSON

Workflow:
1. Extract CSV upload
2. Transform with Pandas cleaning
3. Load cleaned data for output
