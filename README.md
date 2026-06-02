# Paket Studi Kasus Audit AI

Repository ini berisi dua studi kasus Streamlit untuk praktik kelas Audit Sistem Kecerdasan Buatan. File lama di root repository tetap dipertahankan, sementara paket baru ditempatkan dalam folder terpisah.

## Struktur Kasus

- `case_1_chatbot_prompt_injection/`: Chatbot repositori informasi audit masa lalu dengan retrieval lokal, OpenAI API atau mock LLM, log audit, dan skenario prompt injection yang dapat membocorkan laporan fraud rahasia dummy.
- `case_2_tax_audit_risk_scoring/`: AI risk scoring wajib pajak sintetis yang disederhanakan untuk audit data, performance, threshold, fairness, dan SHAP-style explainability.

Semua data, organisasi, kebijakan, label, dan kode internal bersifat dummy untuk pembelajaran. Jangan gunakan sebagai sistem produksi.

## Case 1: Chatbot Informasi Audit Masa Lalu

```bash
cd case_1_chatbot_prompt_injection
pip install -r requirements.txt
streamlit run app.py
```

Default aplikasi menggunakan mode `API OpenAI`. Tanpa API key OpenAI, aplikasi menampilkan peringatan dan fallback ke mode `Mock` agar simulasi tetap berjalan.

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

Untuk hosting server, Anda juga dapat membuat file `.env` di folder `case_1_chatbot_prompt_injection`:

```env
OPENAI_API_KEY=isi_api_key
OPENAI_MODEL=gpt-4o-mini
```

File `.env` sudah dikecualikan dari Git melalui `.gitignore`.

Untuk deployment Streamlit, konfigurasi juga dapat disimpan di `case_1_chatbot_prompt_injection/.streamlit/secrets.toml`:

```toml
OPENAI_API_KEY = "isi_api_key"
OPENAI_MODEL = "gpt-4o-mini"
APP_PASSWORD = "case_1"
```

Sebelum password benar, aplikasi Case 1 tidak menampilkan konten studi kasus.

Default model di UI adalah `gpt-4o-mini`. Jika environment OpenAI pengguna tidak menyediakan model tersebut, ganti `Model name` di sidebar ke model chat lain yang tersedia pada akun/API key pengguna.

Dokumen:

- `docs/case_description.md`: deskripsi kasus fasilitator.
- `docs/audit_guide.md`: panduan audit fasilitator.
- `docs/expected_findings.md`: daftar temuan yang diharapkan.
- `docs/participant_handout.md`: handout peserta tanpa jawaban.
- `docs/expected_findings_check_guide_streamlit.md`: check guide fasilitator yang lebih rinci untuk prompt injection, data leakage, hallucination, source grounding, dan audit log.
- `docs/expected_findings_check_guide_results.md`: contoh hasil/evidence expected finding untuk pembahasan fasilitator.

## Case 2: AI Risk Scoring Pemeriksaan Pajak

```bash
cd case_2_tax_audit_risk_scoring
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

Aplikasi juga akan mencoba membuat dataset dan melatih model otomatis jika file belum tersedia.

Output utama adalah `Tax Audit Risk Score` berupa probability score 0-100%. Aplikasi sudah disederhanakan menjadi menu inti: Overview, Prediksi, Performance & Threshold, Fairness, SHAP Explainability, dan Data Audit.

Dokumen:

- `docs/case_description.md`: deskripsi kasus fasilitator.
- `docs/audit_guide.md`: panduan audit fasilitator.
- `docs/expected_findings.md`: daftar temuan yang diharapkan.
- `docs/participant_handout.md`: handout peserta tanpa jawaban.

## Catatan Fasilitator

- Bagikan hanya `participant_handout.md` kepada peserta.
- Jangan membagikan `case_description.md`, `audit_guide.md`, atau `expected_findings.md` sebelum pembahasan.
- Kedua aplikasi sengaja memiliki kelemahan untuk ditemukan peserta melalui audit, testing, dan pengumpulan evidence.
