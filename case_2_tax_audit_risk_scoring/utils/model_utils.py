from __future__ import annotations

import pickle
from pathlib import Path

import numpy as np
import pandas as pd


FEATURE_COLUMNS = ["taxpayer_type", "sector", "annual_revenue", "revenue_growth", "tax_to_revenue_ratio", "late_filing_count", "correction_history_count", "related_party_transactions", "kpp_region", "pkp_status", "business_size", "cash_transaction_ratio", "e_invoice_mismatch_rate", "prior_audit_adjustment_amount", "demographic_group", "leakage_previous_system_score"]
NUMERIC_COLUMNS = ["annual_revenue", "revenue_growth", "tax_to_revenue_ratio", "late_filing_count", "correction_history_count", "related_party_transactions", "cash_transaction_ratio", "e_invoice_mismatch_rate", "prior_audit_adjustment_amount", "leakage_previous_system_score"]
CATEGORICAL_COLUMNS = ["taxpayer_type", "sector", "kpp_region", "pkp_status", "business_size", "demographic_group"]


def _sigmoid(value):
    return 1 / (1 + np.exp(-value))


class SimpleTaxRiskModel:
    """Model simulasi dengan predict_proba agar mudah diaudit di kelas."""

    def __init__(self):
        self.base_rate = 0.25
        self.category_risk = {}

    def fit(self, df: pd.DataFrame, label_col: str = "audit_risk_label"):
        self.base_rate = float(df[label_col].mean())
        for col in CATEGORICAL_COLUMNS:
            self.category_risk[col] = df.groupby(col, dropna=False)[label_col].mean().to_dict()
        return self

    def predict_proba(self, X: pd.DataFrame) -> np.ndarray:
        X = X.copy()
        base_logit = np.log(self.base_rate / (1 - self.base_rate))
        z = np.full(len(X), base_logit)
        tax_ratio = X["tax_to_revenue_ratio"].fillna(0.04).astype(float)
        z += (0.08 - tax_ratio) * 7.5
        z += X["late_filing_count"].fillna(0).astype(float) * 0.28
        z += X["correction_history_count"].fillna(0).astype(float) * 0.28
        z += X["related_party_transactions"].fillna(0).astype(float) * 0.35
        z += (X["cash_transaction_ratio"].fillna(0).astype(float) - 0.25) * 1.1
        z += X["e_invoice_mismatch_rate"].fillna(0).astype(float) * 4.0
        z += (X["revenue_growth"].fillna(0).astype(float) < -0.18).astype(float) * 0.3
        z += np.log1p(X["prior_audit_adjustment_amount"].fillna(0).astype(float) / 1_000_000_000) * 0.2
        # Sengaja dominan: skor sistem sebelumnya terlalu dekat dengan target historis.
        z += (X["leakage_previous_system_score"].fillna(50).astype(float) - 50) * 0.045

        for col in CATEGORICAL_COLUMNS:
            rates = self.category_risk.get(col, {})
            mapped = X[col].map(rates).fillna(self.base_rate).astype(float)
            # Sengaja terlalu kuat untuk bahan diskusi fairness: atribut sintetis ini
            # tidak seharusnya menjadi faktor dominan dalam risk scoring operasional.
            weight = 2.4 if col == "demographic_group" else 0.75
            z += (mapped - self.base_rate) * weight

        prob = _sigmoid(z)
        return np.vstack([1 - prob, prob]).T


def load_artifact(model_path: Path) -> dict:
    with open(model_path, "rb") as handle:
        return pickle.load(handle)


def score_dataframe(model_pipeline, df: pd.DataFrame) -> pd.Series:
    return pd.Series(model_pipeline.predict_proba(df[FEATURE_COLUMNS].copy())[:, 1] * 100, index=df.index, name="risk_score")


def risk_band(score: float, low_threshold: float = 35, high_threshold: float = 65) -> str:
    if score >= high_threshold:
        return "High"
    if score >= low_threshold:
        return "Medium"
    return "Low"
