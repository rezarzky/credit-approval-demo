from __future__ import annotations

import numpy as np
import pandas as pd


def group_score_summary(df: pd.DataFrame, group_col: str, score_col: str, threshold: float, label_col: str | None = None) -> pd.DataFrame:
    rows = []
    for group_value, group_df in df.groupby(group_col, dropna=False):
        predicted_high = (group_df[score_col] >= threshold).astype(int)
        row = {"group": group_value, "count": len(group_df), "average_score": round(group_df[score_col].mean(), 2), "median_score": round(group_df[score_col].median(), 2), "high_risk_rate_by_threshold": round(predicted_high.mean(), 3)}
        if label_col and label_col in group_df.columns:
            y_true = group_df[label_col].astype(int)
            tn = int(((y_true == 0) & (predicted_high == 0)).sum())
            fp = int(((y_true == 0) & (predicted_high == 1)).sum())
            fn = int(((y_true == 1) & (predicted_high == 0)).sum())
            tp = int(((y_true == 1) & (predicted_high == 1)).sum())
            row["false_positive_rate"] = round(fp / (fp + tn), 3) if (fp + tn) else np.nan
            row["false_negative_rate"] = round(fn / (fn + tp), 3) if (fn + tp) else np.nan
            row["precision"] = round(tp / (tp + fp), 3) if (tp + fp) else np.nan
            row["recall"] = round(tp / (tp + fn), 3) if (tp + fn) else np.nan
        rows.append(row)
    return pd.DataFrame(rows).sort_values("average_score", ascending=False)
