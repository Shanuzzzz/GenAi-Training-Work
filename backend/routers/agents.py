from fastapi import APIRouter
from pydantic import BaseModel

class EligibilityReq(BaseModel):
    user_id: int
    scheme_id: int

router = APIRouter()

@router.post("/eligibility-check")
def eligibility_check(req: EligibilityReq):
    return {"is_eligible": True, "confidence": 0.95, "missing_criteria": []}

@router.post("/explain-benefits")
def explain_benefits(req: EligibilityReq):
    return {"explanation": "This scheme provides...", "simple_language": "You will get..."}
