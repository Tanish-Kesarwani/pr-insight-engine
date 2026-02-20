from dataclasses import dataclass

@dataclass
class MergeRecommendation:
    decision: str
    message: str

class MergeRecommender:
    """
    Provides PR risk level into merge guidance.
    """

    def recommend(self, pr_risk_level: str) -> MergeRecommendation:
        level = pr_risk_level.upper()

        if level == "LOW":
            return MergeRecommendation(
                decision="SAFE_TO_MERGE",
                message="PR appears low risk. Safe to merge with standard review."
            )
        
        elif level == "MEDIUM":
            return MergeRecommendation(
                decision="REVIEW_RECOMMENDED",
                message="PR shows moderate risk signals. Manual review is advised."
            )
        
        elif level == "HIGH":
            return MergeRecommendation(
                decision="HIGH_RISK_REVIEW",
                message="PR has high risk indicators. Thorogh manual review required before merging."
            )
        
        else:
            return MergeRecommendation(
                decision="UNKNOWN",
                message="Unable to determine merge safety."
            )