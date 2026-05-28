from __future__ import annotations

import pandas as pd


def calibration_table(y_true, y_prob, bins: int = 10) -> pd.DataFrame:
    df = pd.DataFrame({"label": y_true, "probability": y_prob})
    df["bin"] = pd.cut(df["probability"], bins=bins, labels=False, include_lowest=True)
    grouped = df.groupby("bin", dropna=False).agg(count=("label", "size"), avg_predicted_probability=("probability", "mean"), observed_rate=("label", "mean")).reset_index()
    grouped["avg_predicted_probability"] = grouped["avg_predicted_probability"].round(3)
    grouped["observed_rate"] = grouped["observed_rate"].round(3)
    grouped["calibration_gap"] = (grouped["avg_predicted_probability"] - grouped["observed_rate"]).round(3)
    return grouped
