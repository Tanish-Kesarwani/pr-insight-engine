from dataclasses import dataclass

@dataclass
class RiskScore:
    file_path: str
    numeric_score: float
    risk_level: str