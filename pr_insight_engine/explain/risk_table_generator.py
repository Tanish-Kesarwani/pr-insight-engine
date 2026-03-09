class RiskTableGenerator:
    """
    Generates a professional table view of file risk scores.
    """

    def generate(self, file_risks):

        # ⭐ Sort files by highest risk score
        sorted_risks = sorted(
            file_risks,
            key=lambda r: r.numeric_score,
            reverse=True
        )

        print("\n============================================================")
        print("                PR FILE RISK TABLE")
        print("============================================================")

        print(f"{'FILE':40} {'SCORE':10} {'LEVEL'}")
        print("-" * 60)

        for risk in sorted_risks:
            file_name = risk.file_path
            score = f"{risk.numeric_score:.2f}"
            level = risk.risk_level

            print(f"{file_name:40} {score:10} {level}")

        print("-" * 60)

        # ⭐ Show top risk file separately
        if sorted_risks:
            top = sorted_risks[0]
            print("\nTop Risk File:")
            print(f"{top.file_path} → {top.risk_level} ({top.numeric_score:.2f})")