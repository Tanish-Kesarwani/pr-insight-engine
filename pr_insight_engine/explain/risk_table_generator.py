class RiskTableGenerator:
    """
    Generates a professional table view of file risk scores.
    """

    def generate(self, file_risks):

        print("\n============================================================")
        print("                PR FILE RISK TABLE")
        print("============================================================")

        print(f"{'FILE':40} {'SCORE':10} {'LEVEL'}")
        print("-" * 60)

        for risk in file_risks:
            file_name = risk.file_path
            score = f"{risk.numeric_score:.2f}"
            level = risk.risk_level

            print(f"{file_name:40} {score:10} {level}")

        print("-" * 60)