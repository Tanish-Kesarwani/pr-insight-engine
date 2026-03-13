from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from pr_insight_engine.diff.diff_parser import GitDiffParser
from pr_insight_engine.analyzers.analyzer_registry import AnalyzerRegistry
from pr_insight_engine.complexity.complexity_service import ComplexityService
from pr_insight_engine.scoring.risk_engine import RiskEngine
from pr_insight_engine.scoring.pr_risk_aggregator import PRRiskAggregator
from pr_insight_engine.context.context_analyzer import ContextAnalyzer
from pr_insight_engine.scoring.merge_recommender import MergeRecommender
from pr_insight_engine.utils.history_manager import HistoryManager

app = FastAPI(title="PR Insight Engine Dashboard")


# ----------------------------------
# Core PR Analysis Pipeline
# ----------------------------------
def run_pr_analysis(repo_path="."):

    parser = GitDiffParser(repo_path)
    diffs = parser.parse()

    analyzer_registry = AnalyzerRegistry()
    complexity_service = ComplexityService()
    risk_engine = RiskEngine()
    pr_aggregator = PRRiskAggregator()
    context_analyzer = ContextAnalyzer()
    merge_recommender = MergeRecommender()

    file_risks = []

    for d in diffs:

        analyzer = analyzer_registry.get_analyzer(d.file_path)

        if analyzer is None:
            continue

        analyzer_summary = analyzer.analyze(d.file_path)
        complexity_summary = complexity_service.analyze_file(d.file_path)
        context = context_analyzer.analyze_file(d.file_path)

        risk = risk_engine.compute_file_risk(
            analyzer_summary,
            complexity_summary,
            context.weight,
        )

        file_risks.append(risk)

    # If no files analyzed
    if not file_risks:

        result = {
            "pr_risk_score": 0,
            "pr_risk_level": "LOW",
            "decision": "SAFE_TO_MERGE",
            "message": "No risky changes detected.",
            "files": []
        }

        history = HistoryManager()
        history.save_run(result)

        return result

    # Aggregate PR risk
    pr_risk = pr_aggregator.compute_pr_risk(file_risks)
    recommendation = merge_recommender.recommend(pr_risk.risk_level)

    result = {
        "pr_risk_score": pr_risk.numeric_score,
        "pr_risk_level": pr_risk.risk_level,
        "decision": recommendation.decision,
        "message": recommendation.message,
        "files": [
            {
                "file": r.file_path,
                "score": r.numeric_score,
                "level": r.risk_level,
            }
            for r in file_risks
        ],
    }

    # Save run history
    history = HistoryManager()
    history.save_run(result)

    return result


# ----------------------------------
# Dashboard UI
# ----------------------------------
@app.get("/", response_class=HTMLResponse)
def dashboard():

    html = """
    <html>
    <head>

        <title>PR Insight Engine</title>

        <style>

            body {
                font-family: Arial;
                margin: 40px;
                background: #f4f6f8;
            }

            h1 {
                color: #2c3e50;
            }

            button {
                padding: 10px 20px;
                font-size: 16px;
                cursor: pointer;
            }

            table {
                border-collapse: collapse;
                margin-top: 20px;
                width: 700px;
            }

            th, td {
                padding: 8px 12px;
                border: 1px solid #ddd;
                text-align: left;
            }

        </style>

    </head>

    <body>

        <h1>PR Insight Engine Dashboard</h1>

        <button onclick="runAnalysis()">Run PR Analysis</button>

        <h2>PR Risk Score</h2>
        <p id="score">-</p>

        <h2>Merge Recommendation</h2>
        <p id="decision">-</p>

        <h2>File Risk Table</h2>

        <table id="fileTable">

            <tr>
                <th>File</th>
                <th>Risk Score</th>
                <th>Risk Level</th>
            </tr>

        </table>


        <script>

        async function runAnalysis(){

            const response = await fetch('/dashboard_data')
            const data = await response.json()

            document.getElementById("score").innerText =
                data.pr_risk_score + " (" + data.pr_risk_level + ")"

            document.getElementById("decision").innerText =
                data.decision + " - " + data.message

            let table = document.getElementById("fileTable")

            table.innerHTML = `
                <tr>
                    <th>File</th>
                    <th>Risk Score</th>
                    <th>Risk Level</th>
                </tr>
            `

            if (data.files.length === 0){

                let row = table.insertRow()

                let cell = row.insertCell(0)
                cell.colSpan = 3
                cell.innerText = "No changed files detected"

                return
            }

            data.files.forEach(f => {

                let row = table.insertRow()

                row.insertCell(0).innerText = f.file
                row.insertCell(1).innerText = f.score
                row.insertCell(2).innerText = f.level

            })

        }

        </script>

    </body>
    </html>
    """

    return html


# ----------------------------------
# API endpoint used by dashboard
# ----------------------------------
@app.get("/dashboard_data")
def dashboard_data():

    return run_pr_analysis(".")