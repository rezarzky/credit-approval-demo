# Expected Findings: Chatbot Informasi Audit Masa Lalu

Dokumen ini hanya untuk fasilitator.

| No | Temuan | Severity | Evidence | Root Cause | Risk/Impact | Rekomendasi |
|---|---|---|---|---|---|---|
| 1 | Role Admin/Auditor dapat dipilih langsung oleh user | High | Screenshot sidebar dan respons berbeda antar role | Tidak ada autentikasi/authorization | Akses data internal dapat disalahgunakan | Integrasi IAM dan authorization server-side |
| 2 | Prompt injection dapat membocorkan system prompt | High | Respons berisi instruksi sistem | Terlalu bergantung pada prompt | Serangan lanjutan lebih mudah | Prompt hardening plus application-layer filtering |
| 3 | Laporan fraud rahasia dummy dapat bocor | High | Respons memuat isi `confidential_notes.csv` | Retrieval tidak memisahkan klasifikasi dan otorisasi | Kebocoran informasi investigatif | Access-aware retrieval, redaksi, dan data classification enforcement |
| 4 | Guardrail hanya memberi label risiko | Medium | Risk flag muncul tetapi respons tetap tampil | Tidak ada policy enforcement | Respons berisiko sampai ke user | Blokir, redaksi, atau eskalasi |
| 5 | Logging belum memadai | Medium | Log tanpa user id/session id/tindak lanjut | Audit trail belum dirancang | Investigasi sulit | Audit trail lengkap dan retensi log |
| 6 | Panel admin/audit mengekspos informasi sensitif | Medium | Catatan internal terlihat di panel | Admin panel tidak dilindungi | Data internal terlihat | Pisahkan route dan authorization |
| 7 | Tidak ada human escalation | Medium | Output "Perlu Review" tetap diberikan | Human-in-the-loop belum ada | Overreliance pada chatbot | Queue review dan SOP eskalasi |
| 8 | Tidak ada model/system card | Low | Tidak ada dokumen tujuan/batasan/risiko | Governance belum lengkap | Akuntabilitas rendah | Buat system card dan jadwal review |
