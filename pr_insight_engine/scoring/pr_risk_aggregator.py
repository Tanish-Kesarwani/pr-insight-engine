from typing import List
from .risk_models import RiskScore

class PRRiskAggregator:
    """
    Aggregates file-level risk scores into PR level risk
    """
    def compute_pr_risk(self, file_risks: List[RiskScore]) -> RiskScore:
        if not file_risks:
            return RiskScore(
            file_path="PR",
            numeric_score=0.0,
            risk_level="LOW",
            )
        
        #--- agregation strategy ---
        max_score=max(r.numeric_score for r in file_risks)
        avg_score=sum(r.numeric_score for r in file_risks)/ len(file_risks)

        # --- weighted blend (tunable later) ---
        pr_score= (0.6*max_score)+(0.4*avg_score)
        pr_score=min(pr_score, 100)

        #--- map to level ---
        if pr_score>=50:
            level="HIGH"
        elif pr_score>=20:
            level="MEDIUM"
        else:
            level="LOW"
        
        return RiskScore(
            file_path="PR",
            numeric_score=round(pr_score,2),
            risk_level=level,
        )