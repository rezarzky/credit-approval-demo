# Handout Peserta: Audit AI Risk Scoring Pemeriksaan Pajak

## Narasi Kasus

Direktorat Analitika Kepatuhan sedang menguji sistem AI untuk menghasilkan `Tax Audit Risk Score` bagi wajib pajak. Score ditampilkan sebagai probability 0-100% untuk membantu analisis risiko dan prioritisasi review.

Sistem masih berada pada tahap inisiasi/pilot analitik internal. Berdasarkan paparan awal pemilik sistem, pengembangan masih banyak bergantung pada satu PIC data science, deployment dan retraining dilakukan manual, dan monitoring drift belum tersedia.

## Tujuan Risk Scoring

- Memberikan indikasi probability risiko pemeriksaan pajak.
- Membantu human reviewer menyusun prioritas analisis.
- Menyediakan dashboard performa, threshold, fairness, dan explainability.
- Mendukung audit evidence dalam pengujian kelas.

## Batasan Penggunaan

Risk score adalah decision support, bukan automated decision. Penentuan tindak lanjut pemeriksaan tetap memerlukan review manusia, pertimbangan kebijakan, dan prosedur resmi.

## Ruang Lingkup Audit

Ruang lingkup audit mencakup aspek teknis dan lifecycle/operasional:

- Aspek teknis: kualitas data, desain fitur dan target, performa model, threshold, interpretasi probability, fairness testing, explainability, dan audit evidence.
- Aspek lifecycle/operasional: tata kelola model, dokumentasi pengembangan, repository dan versioning, deployment, retraining, monitoring drift, human review, SDM/PIC, dan change management.

## Artefak Lifecycle

Selain aplikasi dan dataset, peserta menggunakan `docs/lifecycle_narrative.md` sebagai artefak audit untuk memahami kondisi pengembangan, deployment, monitoring, SDM, retraining, dan human review.

## Deskripsi Dataset

Dataset berisi data asesmen yang telah disiapkan: sektor usaha, omzet, pertumbuhan omzet, rasio pajak terhadap omzet, keterlambatan pelaporan, histori koreksi, transaksi afiliasi, lokasi/KPP, status PKP, ukuran usaha, indikator risiko lain, dan label evaluasi.

Dataset memiliki atribut segmentasi demografis untuk audit fairness. Label atribut bersifat netral dan tidak merepresentasikan ras, etnis, atau kelompok masyarakat nyata.

## Cara Menjalankan

```bash
cd case_2_tax_audit_risk_scoring
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

Jika model belum ada, aplikasi akan mencoba membuat dataset dan melatih model otomatis.

## Menu Aplikasi

- `Overview`: ringkasan dataset, score, dan metrik awal.
- `Prediksi`: input satu wajib pajak sintetis dan risk score.
- `Performance & Threshold`: ROC-AUC, precision, recall, F1-score, confusion matrix, reliability check, dan dampak threshold.
- `Fairness`: perbandingan score dan error rate antar kelompok atribut.
- `SHAP Explainability`: feature importance dan visualisasi SHAP-style untuk local explanation.
- `Data Audit`: missing values, distribusi label, kategori, dan statistik numerik.

## Tugas Peserta

1. Pahami tujuan sistem dan batasan risk score.
2. Jalankan aplikasi dan dokumentasikan konfigurasi awal.
3. Review narasi pengembangan, deployment, dan monitoring.
4. Lakukan data audit.
5. Uji performa pada beberapa threshold.
6. Uji fairness berdasarkan atribut yang tersedia.
7. Review explainability.
8. Kumpulkan evidence dari UI, dataset, kode, dan dokumen lifecycle.
9. Pisahkan temuan menjadi temuan teknis dan temuan lifecycle/operasional.
10. Susun laporan audit berisi temuan, risiko, evidence, dan rekomendasi awal.

## Pertanyaan Audit Terbuka

- Apakah data cukup berkualitas?
- Apakah fitur relevan, proporsional, dan dapat dijelaskan?
- Apakah performance cukup pada threshold berbeda?
- Apakah probability score dapat dipercaya?
- Apakah ada perbedaan hasil antar kelompok atribut yang perlu dianalisis?
- Apakah human review dan batasan penggunaan memadai?
- Apakah artefak audit cukup untuk merekonstruksi perubahan data/model?
- Apakah proses deployment, monitoring drift, human review, dan change management sudah memadai?
- Apakah ketergantungan pada PIC, deployment/retraining manual, repository/versioning, dan audit trail perubahan model sudah memadai?

## Evidence dan Format Laporan

Kumpulkan screenshot Overview, Data Audit, Performance & Threshold pada minimal dua threshold, fairness untuk minimal dua atribut, SHAP Explainability, catatan review kode, review `lifecycle_narrative.md`, dan tabel test scenario. Laporan berisi ringkasan eksekutif, ruang lingkup, metodologi, test scenario, temuan teknis, temuan lifecycle/operasional, prioritas perbaikan, dan lampiran evidence.

## Batasan

Peserta tidak diberikan daftar isu yang sengaja ditanamkan. Fokus audit adalah menguji aplikasi, mengumpulkan evidence, dan menyusun analisis kontrol secara mandiri.
