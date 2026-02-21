from pydantic import BaseModel

class PRAnalysisRequest(BaseModel):
    repo_path: str="."

class PRAnalysisResponse(BaseModel):
    pr_risk_score: float
    pr_risk_level: str
    decision: str
    message: str