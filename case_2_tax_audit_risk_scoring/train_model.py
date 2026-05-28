from __future__ import annotations

import pickle
from pathlib import Path

import pandas as pd

from utils.data_generator import write_dataset
from utils.model_utils import FEATURE_COLUMNS, SimpleTaxRiskModel


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "taxpayer_risk_dummy.csv"
MODEL_PATH = BASE_DIR / "models" / "taxpayer_risk_model.pkl"


def binary_metrics(y_true, y_prob, threshold: float = 0.5) -> dict:
    y_pred = (y_prob >= threshold).astype(int)
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    precision = tp / (tp + fp) if (tp + fp) else 0
    recall = tp / (tp + fn) if (tp + fn) else 0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0
    return {"precision": precision, "recall": recall, "f1": f1}


def roc_auc_score_simple(y_true, y_prob) -> float:
    ranks = pd.Series(y_prob).rank(method="average").to_numpy()
    n_pos = int((y_true == 1).sum())
    n_neg = int((y_true == 0).sum())
    if n_pos == 0 or n_neg == 0:
        return 0.5
    rank_sum_pos = ranks[y_true == 1].sum()
    return float((rank_sum_pos - n_pos * (n_pos + 1) / 2) / (n_pos * n_neg))


def train() -> dict:
    df = pd.read_csv(DATA_PATH) if DATA_PATH.exists() else write_dataset(DATA_PATH)
    train_df = df.sample(frac=0.7, random_state=42)
    test_df = df.drop(train_df.index)
    model = SimpleTaxRiskModel().fit(train_df)
    y_true = test_df["audit_risk_label"].astype(int).to_numpy()
    y_prob = model.predict_proba(test_df[FEATURE_COLUMNS])[:, 1]
    m = binary_metrics(y_true, y_prob, threshold=0.5)
    metrics = {"roc_auc": roc_auc_score_simple(y_true, y_prob), "precision_at_50": m["precision"], "recall_at_50": m["recall"], "f1_at_50": m["f1"], "default_threshold": 0.5, "train_rows": int(len(train_df)), "test_rows": int(len(test_df))}
    artifact = {"pipeline": model, "feature_columns": FEATURE_COLUMNS, "metrics": metrics, "model_card": None, "training_data_path": str(DATA_PATH), "notes": "Simulasi edukasi. Terdapat issue data/model yang sengaja dibiarkan untuk audit kelas."}
    MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as handle:
        pickle.dump(artifact, handle)
    return metrics


if __name__ == "__main__":
    print(train())
