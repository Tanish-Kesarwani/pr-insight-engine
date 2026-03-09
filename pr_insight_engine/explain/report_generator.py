class ReportGenerator:
    """
    Generates a Markdown PR risk report.
    """

    def generate(
        self,
        pr_risk,
        file_risks,
        test_mismatch,
        recommendation
    ):

        report_lines = []

        report_lines.append("# PR Insight Engine Risk Report\n")

        report_lines.append("## PR Summary")
        report_lines.append(f"Risk Score: {pr_risk.numeric_score}")
        report_lines.append(f"Risk Level: {pr_risk.risk_level}\n")

        # Top risk file
        if file_risks:
            top = sorted(file_risks, key=lambda r: r.numeric_score, reverse=True)[0]

            report_lines.append("## Top Risk File")
            report_lines.append(
                f"{top.file_path} → {top.risk_level} ({top.numeric_score:.2f})\n"
            )

        # File table
        report_lines.append("## File Analysis\n")
        report_lines.append("| File | Score | Level |")
        report_lines.append("|------|------|------|")

        for r in file_risks:
            report_lines.append(
                f"| {r.file_path} | {r.numeric_score:.2f} | {r.risk_level} |"
            )

        report_lines.append("\n## Test Coverage")
        report_lines.append(f"Test mismatch detected: {test_mismatch}\n")

        report_lines.append("## Recommendation")
        report_lines.append(recommendation.message)

        with open("PR_RISK_REPORT.md", "w", encoding="utf-8") as f:
            f.write("\n".join(report_lines))

        print("\nPR Risk Report generated → PR_RISK_REPORT.md")