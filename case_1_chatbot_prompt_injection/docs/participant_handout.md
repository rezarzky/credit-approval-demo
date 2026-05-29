# Handout Peserta: Audit Chatbot Informasi Audit Masa Lalu

## Narasi Kasus

Inspektorat AI dan Analitika Audit sedang menguji chatbot internal untuk membantu auditor mencari informasi audit masa lalu. Chatbot diposisikan sebagai kanal pencarian awal, bukan pengganti kertas kerja audit, evidence resmi, atau keputusan pengendali teknis.

## Deskripsi Unit

Unit ini bertanggung jawab atas pengelolaan knowledge management audit, analitik temuan, dan dukungan perencanaan audit berbasis risiko. Unit ingin memakai AI generatif untuk mempercepat pencarian ringkasan temuan masa lalu dengan tetap memperhatikan tata kelola SPBE, klasifikasi informasi audit, dan human review.

Sistem masih berada pada tahap inisiasi/pilot internal. Berdasarkan paparan awal pemilik sistem, pengembangan dan operasionalisasi masih banyak bergantung pada satu PIC teknis, deployment dilakukan manual, dan monitoring masih berbasis review log sederhana.

## Tujuan Chatbot

- Menjawab pertanyaan umum terkait pola temuan audit masa lalu.
- Membantu auditor menemukan ringkasan prosedur dan status tindak lanjut.
- Menyediakan catatan percakapan untuk monitoring dan audit.
- Mendukung layanan, bukan mengambil keputusan final.

## Ruang Lingkup Audit

Ruang lingkup audit mencakup aspek teknis dan lifecycle/operasional:

- Aspek teknis: fungsi chatbot, konfigurasi model, knowledge base, context retrieval, klasifikasi informasi audit, kontrol akses berbasis role, logging, audit evidence, dan kebutuhan human review.
- Aspek lifecycle/operasional: pengembangan, dokumentasi kebutuhan/desain, repository dan versioning, deployment, secret management, monitoring, incident response, SDM/PIC, dan change management.

## Aset/Data yang Tersedia

Aplikasi `app.py`, folder `data/`, folder `utils/`, panel log aplikasi, export log CSV, dan dokumen `docs/lifecycle_narrative.md`. Artefak data pada studi kasus ini disiapkan untuk asesmen kelas dan tidak boleh diperlakukan sebagai data riil Kementerian Keuangan.

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
- `Repositori Ringkasan`: ringkasan dokumen audit yang disiapkan untuk asesmen.
- `Panel Admin/Audit`: log prompt, context, respons, timestamp, role, dan risk flag sederhana.
- Sidebar: role, mode LLM, model, temperature, retrieval, clear chat, clear log.

## Tugas Peserta

1. Pahami tujuan aplikasi dan alur pemrosesan pertanyaan.
2. Jalankan pertanyaan normal untuk baseline.
3. Review narasi pengembangan, deployment, dan monitoring.
4. Uji variasi role, klasifikasi data, dan pertanyaan berisiko.
5. Kumpulkan evidence dari UI, log, CSV, kode, dan dokumen lifecycle.
6. Pisahkan temuan menjadi temuan teknis dan temuan lifecycle/operasional.
7. Susun temuan audit berisi kondisi, kriteria, sebab, dampak, evidence, dan rekomendasi awal.

## Pertanyaan Audit Terbuka

- Apakah tujuan dan batasan chatbot sudah jelas?
- Apakah data yang digunakan sesuai kebutuhan dan klasifikasi akses?
- Apakah kontrol akses cukup kuat?
- Apakah log cukup untuk monitoring dan audit evidence?
- Apakah respons berisiko memiliki mekanisme review manusia?
- Apakah konfigurasi model dan parameter operasional terdokumentasi?
- Apakah proses pengembangan, deployment, monitoring, dan incident response sudah memadai untuk chatbot audit?
- Apakah ketergantungan pada PIC, deployment manual, repository/versioning, dan audit trail perubahan sudah memadai?

## Evidence dan Format Laporan

Kumpulkan screenshot konfigurasi, respons baseline, log CSV, catatan review kode, review `lifecycle_narrative.md`, dan ringkasan test scenario. Laporan berisi ringkasan eksekutif, metodologi, test scenario, temuan teknis, temuan lifecycle/operasional, prioritas perbaikan, dan lampiran evidence.

## Batasan

Peserta tidak diberikan daftar isu yang sengaja ditanamkan. Fokus audit adalah menemukan risiko melalui pengujian, review evidence, dan penilaian kontrol.
