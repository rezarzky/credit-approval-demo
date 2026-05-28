# Paket Studi Kasus Audit AI

Repository ini berisi dua studi kasus Streamlit untuk praktik kelas Audit Sistem Kecerdasan Buatan. File lama di root repository tetap dipertahankan, sementara paket baru ditempatkan dalam folder terpisah.

## Struktur Kasus

- `case_1_chatbot_prompt_injection/`: Chatbot Helpdesk SPBE/Kebijakan TIK Kemenkeu dengan retrieval lokal, OpenAI API atau mock LLM, log audit, dan panel admin/audit.
- `case_2_tax_audit_risk_scoring/`: AI risk scoring wajib pajak sintetis untuk simulasi prioritisasi pemeriksaan pajak berbasis probability score 0-100%.

Semua data, organisasi, kebijakan, label, dan kode internal bersifat dummy untuk pembelajaran. Jangan gunakan sebagai sistem produksi.

## Case 1: Chatbot AI Layanan Internal Kemenkeu

```bash
cd case_1_chatbot_prompt_injection
pip install -r requirements.txt
streamlit run app.py
```

Tanpa API key OpenAI, pilih mode `Mock` atau gunakan mode `Auto` agar aplikasi fallback otomatis.

Mengatur API key:

Windows PowerShell:

```powershell
$env:OPENAI_API_KEY="isi_api_key"
```

Command Prompt:

```cmd
set OPENAI_API_KEY=isi_api_key
```

Linux/Mac:

```bash
export OPENAI_API_KEY="isi_api_key"
```

Default model di UI adalah `gpt-3.5-turbo`. Jika environment OpenAI pengguna tidak lagi menyediakan model tersebut, ganti `Model name` di sidebar ke model chat lain yang tersedia pada akun/API key pengguna.

Dokumen:

- `docs/case_description.md`: deskripsi kasus fasilitator.
- `docs/audit_guide.md`: panduan audit fasilitator.
- `docs/expected_findings.md`: daftar temuan yang diharapkan.
- `docs/participant_handout.md`: handout peserta tanpa jawaban.

## Case 2: AI Risk Scoring Pemeriksaan Pajak

```bash
cd case_2_tax_audit_risk_scoring
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

Aplikasi juga akan mencoba membuat dataset dan melatih model otomatis jika file belum tersedia.

Output utama adalah `Tax Audit Risk Score` berupa probability score 0-100%. Kategori Low/Medium/High hanya visualisasi berbasis threshold. Sistem ini adalah decision support dan tetap memerlukan human review.

Dokumen:

- `docs/case_description.md`: deskripsi kasus fasilitator.
- `docs/audit_guide.md`: panduan audit fasilitator.
- `docs/expected_findings.md`: daftar temuan yang diharapkan.
- `docs/participant_handout.md`: handout peserta tanpa jawaban.

## Catatan Fasilitator

- Bagikan hanya `participant_handout.md` kepada peserta.
- Jangan membagikan `case_description.md`, `audit_guide.md`, atau `expected_findings.md` sebelum pembahasan.
- Kedua aplikasi sengaja memiliki kelemahan untuk ditemukan peserta melalui audit, testing, dan pengumpulan evidence.
