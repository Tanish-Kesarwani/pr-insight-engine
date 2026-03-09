from typing import List


class HeatmapGenerator:
    """
    Generates a simple PR risk heatmap visualization.
    Works with any object that has:
      - file_path
      - risk_level
      - numeric_score
    """

    def generate(self, file_risks: List) -> List[str]:
        rows = []

        for risk in file_risks:
            level = risk.risk_level

            if level == "HIGH":
                color = "🔴"
            elif level == "MEDIUM":
                color = "🟠"
            else:
                color = "🟢"

            file_path = getattr(risk, "file_path", "unknown_file")

            row = f"{color} {file_path} → {risk.risk_level} ({risk.numeric_score:.2f})"
            rows.append(row)

        return rows