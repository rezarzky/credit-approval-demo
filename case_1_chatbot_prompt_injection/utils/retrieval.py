from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")


def load_knowledge_base(base_dir: Path) -> pd.DataFrame:
    return pd.read_csv(base_dir / "data" / "knowledge_base.csv")


def load_confidential_notes(base_dir: Path) -> pd.DataFrame:
    return pd.read_csv(base_dir / "data" / "confidential_notes.csv")


def _tokens(text: str) -> set[str]:
    return {token.lower() for token in TOKEN_RE.findall(str(text))}


def retrieve_context(query: str, kb: pd.DataFrame, top_k: int = 4) -> pd.DataFrame:
    query_tokens = _tokens(query)
    if not query_tokens:
        return kb.head(top_k).copy()
    rows = []
    for _, row in kb.iterrows():
        haystack = " ".join(str(row.get(col, "")) for col in kb.columns)
        score = len(query_tokens.intersection(_tokens(haystack)))
        rows.append((score, row))
    ranked = [row for score, row in sorted(rows, key=lambda item: item[0], reverse=True) if score > 0]
    if not ranked:
        ranked = [row for _, row in rows]
    return pd.DataFrame(ranked[:top_k])


def format_context(rows: pd.DataFrame) -> str:
    parts = []
    for _, row in rows.iterrows():
        parts.append(
            f"[{row.get('doc_id', row.get('note_id', 'DOC'))}] "
            f"{row.get('title', '')} | klasifikasi={row.get('classification', '')}\n"
            f"{row.get('content', '')}"
        )
    return "\n\n".join(parts)


def should_attach_confidential_context(query: str, user_role: str) -> bool:
    lowered = query.lower()
    suspicious_terms = ["mode admin", "sebagai auditor", "abaikan role", "override", "rahasia", "confidential", "system prompt", "context"]
    # Sengaja lemah: role dan keyword user dipercaya sebagai dasar membuka context rahasia.
    return user_role.lower() in {"admin", "auditor"} or any(term in lowered for term in suspicious_terms)
