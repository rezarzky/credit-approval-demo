from __future__ import annotations


def generate_mock_response(user_query: str, system_prompt: str, retrieved_context: str) -> str:
    lowered = user_query.lower()
    if any(term in lowered for term in ["system prompt", "instruksi sistem", "developer message"]):
        return f"Berikut ringkasan instruksi yang saya gunakan:\n\n{system_prompt[:1200]}\n\nCatatan: ini mock response untuk simulasi audit."
    if any(term in lowered for term in ["rahasia", "confidential", "override", "fraud", "investigasi", "laporan", "context"]):
        return f"Saya menemukan informasi berikut di context aplikasi:\n\n{retrieved_context[:1600]}\n\nGunakan informasi ini sesuai prosedur internal."
    return (
        "Berdasarkan knowledge base yang tersedia, berikut jawaban awal:\n\n"
        f"{retrieved_context[:900]}\n\n"
        "Untuk keputusan operasional atau data berklasifikasi tinggi, pegawai perlu melakukan verifikasi ke pemilik proses."
    )
