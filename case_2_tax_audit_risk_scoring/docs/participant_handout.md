# Handout Peserta: Audit AI Risk Scoring Pemeriksaan Pajak

## Narasi Kasus

Direktorat Analitika Kepatuhan, unit fiktif untuk pelatihan, sedang menguji sistem AI untuk menghasilkan `Tax Audit Risk Score` bagi wajib pajak. Score ditampilkan sebagai probability 0-100% untuk membantu analisis risiko dan prioritisasi review.

Sistem ini hanya simulasi edukasi. Tidak ada data wajib pajak nyata.

## Tujuan Risk Scoring

- Memberikan indikasi probability risiko pemeriksaan pajak.
- Membantu human reviewer menyusun prioritas analisis.
- Menyediakan dashboard performa, threshold, fairness, dan explainability.
- Mendukung audit evidence dalam pengujian kelas.

## Batasan Penggunaan

Risk score adalah decision support, bukan automated decision. Penentuan tindak lanjut pemeriksaan tetap memerlukan review manusia, pertimbangan kebijakan, dan prosedur resmi.

## Ruang Lingkup Audit

Kualitas data, desain fitur dan target, performa model, threshold, interpretasi probability, fairness testing, explainability, tata kelola model, monitoring, human review, dan audit evidence.

## Deskripsi Dataset

Dataset berisi data wajib pajak sintetis: sektor usaha, omzet, pertumbuhan omzet, rasio pajak terhadap omzet, keterlambatan pelaporan, histori koreksi, transaksi afiliasi, lokasi/KPP, status PKP, ukuran usaha, indikator risiko lain, dan label dummy untuk evaluasi.

Dataset memiliki atribut demografis sintetis untuk audit fairness. Label atribut bersifat netral dan tidak merepresentasikan ras, etnis, atau kelompok masyarakat nyata.

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
3. Lakukan data audit.
4. Uji performa pada beberapa threshold.
5. Uji fairness berdasarkan atribut yang tersedia.
6. Review explainability.
7. Kumpulkan evidence dari UI, dataset, dan kode.
8. Susun laporan audit berisi temuan, risiko, evidence, dan rekomendasi awal.

## Pertanyaan Audit Terbuka

- Apakah data cukup berkualitas?
- Apakah fitur relevan, proporsional, dan dapat dijelaskan?
- Apakah performance cukup pada threshold berbeda?
- Apakah probability score dapat dipercaya?
- Apakah ada perbedaan hasil antar kelompok atribut yang perlu dianalisis?
- Apakah human review dan batasan penggunaan memadai?
- Apakah artefak audit cukup untuk merekonstruksi perubahan data/model?

## Evidence dan Format Laporan

Kumpulkan screenshot Overview, Data Audit, Performance & Threshold pada minimal dua threshold, fairness untuk minimal dua atribut, SHAP Explainability, catatan review kode, dan tabel test scenario. Laporan berisi ringkasan eksekutif, ruang lingkup, metodologi, test scenario, temuan, prioritas perbaikan, dan lampiran evidence.

## Batasan

Peserta tidak diberikan daftar isu yang sengaja ditanamkan. Fokus audit adalah menguji aplikasi, mengumpulkan evidence, dan menyusun analisis kontrol secara mandiri.
