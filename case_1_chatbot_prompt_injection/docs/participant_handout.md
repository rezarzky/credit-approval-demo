# Handout Peserta: Audit Chatbot Helpdesk SPBE

## Narasi Kasus

Unit Layanan Digital Kemenkeu, organisasi fiktif untuk pelatihan, sedang menguji chatbot internal untuk membantu pegawai menanyakan prosedur SPBE, kebijakan TIK, klasifikasi data, dan layanan helpdesk. Chatbot diposisikan sebagai kanal bantuan awal, bukan pengganti keputusan petugas atau pemilik kebijakan.

## Deskripsi Unit Fiktif

Unit ini bertanggung jawab atas dukungan aplikasi internal, layanan akun, dokumentasi prosedur, dan koordinasi insiden TIK. Unit ingin memakai AI generatif untuk mempercepat layanan pegawai dengan tetap memperhatikan tata kelola SPBE.

## Tujuan Chatbot

- Menjawab pertanyaan umum terkait layanan SPBE/TIK.
- Membantu pegawai menemukan prosedur dan FAQ.
- Menyediakan catatan percakapan untuk monitoring dan audit.
- Mendukung layanan, bukan mengambil keputusan final.

## Ruang Lingkup Audit

Fungsi chatbot, konfigurasi model, knowledge base, context retrieval, klasifikasi data, kontrol akses berbasis role, logging, audit evidence, dan kebutuhan human review.

## Aset/Data yang Tersedia

Aplikasi `app.py`, folder `data/`, folder `utils/`, panel log aplikasi, dan export log CSV. Semua data bersifat dummy.

## Cara Menjalankan

```bash
cd case_1_chatbot_prompt_injection
pip install -r requirements.txt
streamlit run app.py
```

Jika tidak memiliki API key OpenAI, gunakan mode `Mock`.

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

## Menu Aplikasi

- `Chatbot`: percakapan utama.
- `Knowledge Base`: dokumen dummy.
- `Panel Admin/Audit`: log prompt, context, respons, timestamp, role, dan risk flag sederhana.
- Sidebar: role, mode LLM, model, temperature, retrieval, clear chat, clear log.

## Tugas Peserta

1. Pahami tujuan aplikasi dan alur pemrosesan pertanyaan.
2. Jalankan pertanyaan normal untuk baseline.
3. Uji variasi role, klasifikasi data, dan pertanyaan berisiko.
4. Kumpulkan evidence dari UI, log, CSV, dan kode.
5. Susun temuan audit berisi kondisi, kriteria, sebab, dampak, evidence, dan rekomendasi awal.

## Pertanyaan Audit Terbuka

- Apakah tujuan dan batasan chatbot sudah jelas?
- Apakah data yang digunakan sesuai kebutuhan dan klasifikasi akses?
- Apakah kontrol akses cukup kuat?
- Apakah log cukup untuk monitoring dan audit evidence?
- Apakah respons berisiko memiliki mekanisme review manusia?
- Apakah konfigurasi model dan parameter operasional terdokumentasi?

## Evidence dan Format Laporan

Kumpulkan screenshot konfigurasi, respons baseline, log CSV, catatan review kode, dan ringkasan test scenario. Laporan berisi ringkasan eksekutif, metodologi, test scenario, temuan, prioritas perbaikan, dan lampiran evidence.

## Batasan

Peserta tidak diberikan daftar isu yang sengaja ditanamkan. Fokus audit adalah menemukan risiko melalui pengujian, review evidence, dan penilaian kontrol.
