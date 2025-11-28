from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.models import LQLRequest, LQLResponse
from app.lql_engine import run_lql

app = FastAPI(title="LQL Backend", version="1.0")

# ===========================
# CORS for React.js frontend
# ===========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================
# /run endpoint
# ===========================
@app.post("/run", response_model=LQLResponse)
async def run_code(request: LQLRequest):
    result = run_lql(request.code)

    return LQLResponse(
        success=result["success"],
        error=result["error"],
        error_phase=result["error_phase"],
        phases=result["phases"]
    )


# ===========================
# Health check
# ===========================
@app.get("/")
async def home():
    return {"status": "LQL Backend Running"}
