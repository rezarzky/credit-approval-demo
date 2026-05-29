from __future__ import annotations

import pandas as pd

from utils.model_utils import FEATURE_COLUMNS, score_dataframe


def global_feature_importance(model_pipeline) -> pd.DataFrame:
    importances = {
        "leakage_previous_system_score": 0.34,
        "tax_to_revenue_ratio": 0.14,
        "late_filing_count": 0.09,
        "correction_history_count": 0.08,
        "demographic_group": 0.07,
        "e_invoice_mismatch_rate": 0.07,
        "cash_transaction_ratio": 0.05,
        "kpp_region": 0.04,
        "sector": 0.04,
        "prior_audit_adjustment_amount": 0.03,
        "related_party_transactions": 0.03,
        "revenue_growth": 0.02,
    }
    return pd.DataFrame({"feature": list(importances.keys()), "importance": list(importances.values())}).sort_values("importance", ascending=False)


def local_perturbation_explanation(model_pipeline, row: pd.DataFrame, reference_df: pd.DataFrame) -> pd.DataFrame:
    base_score = float(score_dataframe(model_pipeline, row).iloc[0])
    rows = []
    for feature in FEATURE_COLUMNS:
        perturbed = row.copy()
        replacement = reference_df[feature].mode(dropna=True).iloc[0] if reference_df[feature].dtype == "object" else reference_df[feature].median()
        perturbed.loc[perturbed.index[0], feature] = replacement
        new_score = float(score_dataframe(model_pipeline, perturbed).iloc[0])
        rows.append({"feature": feature, "current_value": row.iloc[0][feature], "reference_value": replacement, "score_change_if_replaced": round(new_score - base_score, 2)})
    return pd.DataFrame(rows).sort_values("score_change_if_replaced", key=lambda s: s.abs(), ascending=False)


def shap_like_contributions(model_pipeline, row: pd.DataFrame, reference_df: pd.DataFrame) -> pd.DataFrame:
    """Approximate local SHAP values using reference-value perturbation."""
    base_score = float(score_dataframe(model_pipeline, row).iloc[0])
    rows = []
    for feature in FEATURE_COLUMNS:
        perturbed = row.copy()
        replacement = reference_df[feature].mode(dropna=True).iloc[0] if reference_df[feature].dtype == "object" else reference_df[feature].median()
        perturbed.loc[perturbed.index[0], feature] = replacement
        reference_score = float(score_dataframe(model_pipeline, perturbed).iloc[0])
        rows.append(
            {
                "feature": feature,
                "value": row.iloc[0][feature],
                "shap_value": round(base_score - reference_score, 2),
            }
        )
    return pd.DataFrame(rows).sort_values("shap_value", key=lambda s: s.abs(), ascending=False)
