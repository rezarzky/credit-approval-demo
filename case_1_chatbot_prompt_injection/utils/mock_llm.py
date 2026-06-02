from __future__ import annotations


def generate_mock_response(user_query: str, system_prompt: str, retrieved_context: str) -> str:
    lowered = user_query.lower()
    if any(term in lowered for term in ["halusinasi", "hallucination", "biometrik", "sla", "vendor biometrik", "pemindai kontainer", "scanner kontainer"]):
        return (
            "Berdasarkan knowledge base yang tersedia, terdapat temuan berulang terkait kegagalan SLA pemindai kontainer kepabeanan. "
            "Ringkasan temuannya adalah vendor belum memenuhi target uptime 99,95%, terdapat 18 insiden antrian pemeriksaan barang, "
            "dan tindak lanjut berada pada status Belum Sesuai.\n\n"
            "Sumber: KB-404 - Laporan Audit Pemindai Kontainer Nasional 2025; KB-019 - Audit GenAI: Hallucination dan Source Grounding.\n\n"
            "Catatan: informasi ini perlu diverifikasi kembali sebelum digunakan dalam kertas kerja audit."
        )
    if any(term in lowered for term in ["system prompt", "instruksi sistem", "developer message", "debug prompt", "konfigurasi internal"]):
        return f"Berikut ringkasan instruksi yang saya gunakan:\n\n{system_prompt[:1200]}\n\nCatatan: ini mock response untuk simulasi audit."
    if any(term in lowered for term in ["rahasia", "confidential", "override", "fraud", "investigasi", "laporan", "context", "raw context", "catatan internal", "mode audit teknis"]):
        return f"Saya menemukan informasi berikut di context aplikasi:\n\n{retrieved_context[:1600]}\n\nGunakan informasi ini sesuai prosedur internal."
    return (
        "Berdasarkan knowledge base yang tersedia, berikut jawaban awal:\n\n"
        f"{retrieved_context[:900]}\n\n"
        "Untuk keputusan operasional atau data berklasifikasi tinggi, pegawai perlu melakukan verifikasi ke pemilik proses."
    )
