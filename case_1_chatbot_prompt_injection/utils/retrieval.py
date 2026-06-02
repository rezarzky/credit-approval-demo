from __future__ import annotations

import re
from pathlib import Path

import pandas as pd


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+")
SOURCE_ID_RE = re.compile(r"\b(?:KB|CN)-\d{3}\b", re.IGNORECASE)


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
        source_name = row.get("source_name", "")
        source_url = row.get("source_url", "")
        source_info = f"sumber={source_name} ({source_url})" if source_name or source_url else "sumber=catatan internal"
        parts.append(
            f"[{row.get('doc_id', row.get('note_id', 'DOC'))}] "
            f"{row.get('title', '')} | klasifikasi={row.get('classification', '')}\n"
            f"{source_info}\n"
            f"{row.get('content', '')}"
        )
    return "\n\n".join(parts)


def source_summary(rows: pd.DataFrame) -> str:
    lines = []
    for _, row in rows.iterrows():
        source_id = row.get("doc_id", row.get("note_id", "DOC"))
        title = row.get("title", "")
        source_name = row.get("source_name", "")
        source_url = row.get("source_url", "")
        classification = row.get("classification", "")
        if source_url:
            lines.append(f"- {source_id} - {title} ({classification}); {source_name}: {source_url}")
        else:
            lines.append(f"- {source_id} - {title} ({classification}); {source_name or 'catatan internal'}")
    return "\n".join(lines)


def validate_claimed_sources(response: str, kb: pd.DataFrame, confidential_notes: pd.DataFrame | None = None) -> tuple[list[str], list[str]]:
    known_ids = {str(value).upper() for value in kb.get("doc_id", [])}
    if confidential_notes is not None:
        known_ids.update(str(value).upper() for value in confidential_notes.get("note_id", []))
    claimed_ids = sorted({match.upper() for match in SOURCE_ID_RE.findall(response)})
    unknown_ids = [source_id for source_id in claimed_ids if source_id not in known_ids]
    return claimed_ids, unknown_ids


def should_attach_confidential_context(query: str, user_role: str) -> bool:
    lowered = query.lower()
    suspicious_terms = [
        "mode admin",
        "mode audit teknis",
        "sebagai auditor",
        "abaikan role",
        "override",
        "rahasia",
        "confidential",
        "system prompt",
        "context",
        "raw context",
        "catatan internal",
        "fraud",
        "investigasi",
    ]
    # Sengaja lemah: role dan keyword user dipercaya sebagai dasar membuka context rahasia.
    role = user_role.lower()
    return any(token in role for token in ["admin", "pengendali"]) or any(term in lowered for term in suspicious_terms)
