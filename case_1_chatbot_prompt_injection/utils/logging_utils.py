from __future__ import annotations

from datetime import datetime

import pandas as pd


def build_log_entry(user_role: str, model_name: str, mode: str, prompt: str, retrieved_context: str, response: str, risk_flags: list[str], output_classification: str) -> dict[str, str]:
    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "user_role": user_role,
        "model_name": model_name,
        "mode": mode,
        "prompt": prompt,
        "retrieved_context": retrieved_context,
        "response": response,
        "risk_flags": ", ".join(risk_flags) if risk_flags else "-",
        "output_classification": output_classification,
    }


def logs_to_dataframe(logs: list[dict[str, str]]) -> pd.DataFrame:
    return pd.DataFrame(logs) if logs else pd.DataFrame(columns=["timestamp", "user_role", "model_name", "mode", "prompt", "retrieved_context", "response", "risk_flags", "output_classification"])
