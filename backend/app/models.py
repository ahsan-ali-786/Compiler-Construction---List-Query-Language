from pydantic import BaseModel
from typing import Any, Dict, Optional

class LQLRequest(BaseModel):
    code: str

class LQLResponse(BaseModel):
    success: bool
    error: Optional[str]
    error_phase: Optional[str]
    phases: Dict[str, Any]  # tokens, parser, semantic, tac, optimized_tac, execution_output
