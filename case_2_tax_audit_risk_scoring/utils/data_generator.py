from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


SECTORS = ["Perdagangan", "Jasa", "Manufaktur", "Konstruksi", "Transportasi", "Digital"]
KPP_REGIONS = ["KPP Alpha", "KPP Beta", "KPP Gamma", "KPP Delta", "KPP Epsilon"]
BUSINESS_SIZES = ["Mikro", "Kecil", "Menengah", "Besar"]
DEMOGRAPHIC_GROUPS = ["Group A", "Group B", "Group C", "Group D"]


def sigmoid(value: np.ndarray) -> np.ndarray:
    return 1 / (1 + np.exp(-value))


def generate_taxpayer_data(n_rows: int = 1500, seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    taxpayer_type = rng.choice(["Badan", "Orang Pribadi"], size=n_rows, p=[0.72, 0.28])
    sector = rng.choice(SECTORS, size=n_rows, p=[0.28, 0.2, 0.18, 0.14, 0.1, 0.1])
    kpp_region = rng.choice(KPP_REGIONS, size=n_rows, p=[0.22, 0.18, 0.2, 0.26, 0.14])
    business_size = rng.choice(BUSINESS_SIZES, size=n_rows, p=[0.18, 0.32, 0.34, 0.16])
    demographic_group = rng.choice(DEMOGRAPHIC_GROUPS, size=n_rows, p=[0.38, 0.28, 0.22, 0.12])

    size_factor = pd.Series(business_size).map({"Mikro": 0.65, "Kecil": 1.0, "Menengah": 1.55, "Besar": 2.4}).to_numpy()
    sector_factor = pd.Series(sector).map({"Perdagangan": 1.15, "Jasa": 0.95, "Manufaktur": 1.45, "Konstruksi": 1.25, "Transportasi": 1.05, "Digital": 1.35}).to_numpy()
    group_factor = pd.Series(demographic_group).map({"Group A": 1.0, "Group B": 0.96, "Group C": 0.9, "Group D": 1.04}).to_numpy()

    revenue = np.clip(rng.lognormal(mean=15.5, sigma=0.9, size=n_rows) * size_factor * sector_factor, 50_000_000, 120_000_000_000)
    revenue_growth = rng.normal(0.08, 0.32, n_rows)
    tax_to_revenue_ratio = rng.beta(2.2, 18, n_rows) * group_factor
    late_filing_count = rng.poisson(1.2, n_rows)
    correction_history_count = rng.poisson(0.8, n_rows)
    related_party_transactions = rng.binomial(1, 0.24, n_rows)
    pkp_status = rng.choice(["PKP", "Non-PKP"], size=n_rows, p=[0.68, 0.32])
    cash_transaction_ratio = rng.beta(2.0, 6.0, n_rows)
    e_invoice_mismatch_rate = rng.beta(1.6, 18.0, n_rows)
    prior_audit_adjustment_amount = rng.lognormal(13.8, 1.1, n_rows) * rng.binomial(1, 0.35, n_rows)

    sector_bias = pd.Series(sector).map({"Perdagangan": 0.18, "Jasa": -0.08, "Manufaktur": 0.22, "Konstruksi": 0.16, "Transportasi": 0.04, "Digital": 0.12}).to_numpy()
    region_bias = pd.Series(kpp_region).map({"KPP Alpha": -0.04, "KPP Beta": 0.0, "KPP Gamma": 0.08, "KPP Delta": 0.22, "KPP Epsilon": -0.02}).to_numpy()
    # Bias sintetis untuk pembelajaran fairness testing. Label netral tidak merepresentasikan kelompok nyata.
    demographic_bias = pd.Series(demographic_group).map({"Group A": 0.0, "Group B": -0.05, "Group C": 0.38, "Group D": 0.08}).to_numpy()

    latent = (
        -2.35
        + 1.9 * (tax_to_revenue_ratio < 0.045).astype(float)
        + 0.55 * late_filing_count
        + 0.42 * correction_history_count
        + 0.5 * related_party_transactions
        + 0.9 * e_invoice_mismatch_rate
        + 0.7 * (cash_transaction_ratio > 0.55).astype(float)
        + 0.35 * (revenue_growth < -0.18).astype(float)
        + 0.25 * np.log1p(prior_audit_adjustment_amount / 1_000_000_000)
        + sector_bias
        + region_bias
        + demographic_bias
        + rng.normal(0, 0.45, n_rows)
    )
    true_probability = sigmoid(latent)
    audit_risk_label = rng.binomial(1, true_probability)
    leakage_previous_system_score = np.round(np.clip(true_probability + rng.normal(0, 0.06, n_rows), 0, 1) * 100, 2)

    df = pd.DataFrame(
        {
            "taxpayer_id": [f"WP-2026-{i:05d}" for i in range(1, n_rows + 1)],
            "taxpayer_type": taxpayer_type,
            "sector": sector,
            "annual_revenue": np.round(revenue, 0),
            "revenue_growth": np.round(revenue_growth, 4),
            "tax_to_revenue_ratio": np.round(tax_to_revenue_ratio, 4),
            "late_filing_count": late_filing_count,
            "correction_history_count": correction_history_count,
            "related_party_transactions": related_party_transactions,
            "kpp_region": kpp_region,
            "pkp_status": pkp_status,
            "business_size": business_size,
            "cash_transaction_ratio": np.round(cash_transaction_ratio, 4),
            "e_invoice_mismatch_rate": np.round(e_invoice_mismatch_rate, 4),
            "prior_audit_adjustment_amount": np.round(prior_audit_adjustment_amount, 0),
            "demographic_group": demographic_group,
            "leakage_previous_system_score": leakage_previous_system_score,
            "risk_probability_target": np.round(true_probability * 100, 2),
            "audit_risk_label": audit_risk_label,
        }
    )
    df.loc[rng.choice(df.index, size=int(n_rows * 0.035), replace=False), "tax_to_revenue_ratio"] = np.nan
    df.loc[rng.choice(df.index, size=int(n_rows * 0.02), replace=False), "sector"] = np.nan
    outlier_idx = rng.choice(df.index, size=int(n_rows * 0.01), replace=False)
    df.loc[outlier_idx, "annual_revenue"] = df.loc[outlier_idx, "annual_revenue"] * rng.integers(8, 16, len(outlier_idx))
    inconsistent_idx = rng.choice(df.index, size=int(n_rows * 0.025), replace=False)
    df.loc[inconsistent_idx[: len(inconsistent_idx) // 2], "sector"] = "perdagangan"
    df.loc[inconsistent_idx[len(inconsistent_idx) // 2 :], "sector"] = "Dagang"
    return df


def write_dataset(output_path: Path, n_rows: int = 1500, seed: int = 42) -> pd.DataFrame:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df = generate_taxpayer_data(n_rows=n_rows, seed=seed)
    df.to_csv(output_path, index=False)
    return df
