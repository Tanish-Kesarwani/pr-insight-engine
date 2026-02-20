from typing import List
from pr_insight_engine.analyzers.analyzer_models import AnalyzerSummary
from pr_insight_engine.complexity.complexity_models import ComplexitySummary
from pr_insight_engine.context.context_models import FileContext
from .explanation_models import RiskExplanation

class ExplanationEngine:
    """
    Generates human-readable explanations for risk signals.
    """

    def generate_file_explanation(
            self,
            analyzer_summary: AnalyzerSummary,
            complexity_summary: ComplexitySummary,
            context: FileContext,
    ) -> RiskExplanation:
        
        messages: List[str] = []
        
        # --- analyzer findings ---
        if analyzer_summary.total_findings > 0:
            messages.append(
                f"{analyzer_summary.total_findings} static analysis finding(s) detected."
            )

        # --- high complexity ---
        if complexity_summary.average_complexity >= 10:
            messages.append(
                "High cyclomatic complexity detected; code maybe harder to maintain"

                )
        elif complexity_summary.max_complexity >= 6:
            messages.append(
                "Moderate complexity detected in modified code."
                )

        # --- Context signals ---
        if "sensitive_module" in context.tags:
            messages.append(
                "Sensitive module modified; requires careful review."
            )
        elif "core_module" in context.tags:
            messages.append(
                "Core service/module impacted by changes."
            
            )
        elif "low_risk_area" in context.tags:
            messages.append(
                "Changes are in a low-risk area."
            ) 

        # --- clean case ---   
        if not messages:
            messages.append("No significant risk signals detected.")

        return RiskExplanation(
            file_path=analyzer_summary.file_path,
            messages=messages,
        ) 
    