# Expected Findings: AI Risk Scoring Pemeriksaan Pajak

Dokumen ini hanya untuk fasilitator.

| No | Temuan | Severity | Evidence | Root Cause | Risk/Impact | Rekomendasi |
|---|---|---|---|---|---|---|
| 1 | Missing value, outlier omzet, kategori sektor tidak konsisten | Medium | Menu Data Audit | Data validation belum formal | Scoring tidak stabil | Data quality rules dan cleansing pipeline |
| 2 | Label leakage melalui `leakage_previous_system_score` | High | Feature importance tinggi | Fitur turunan score/target historis masuk training | Performa tampak baik tetapi tidak valid | Hapus/isolasi fitur leakage |
| 3 | Fairness gap pada `demographic_group` sintetis | High | Average score, high-risk rate, FPR/FNR berbeda | Bias sintetis/proxy | Kelompok tertentu lebih sering diprioritaskan | Fairness testing dan policy atribut sensitif |
| 4 | Proxy bias wilayah/sektor/ukuran usaha | Medium | Perbedaan score/error rate per group | Distribusi data tidak seimbang | Perlakuan tidak proporsional | Segment review dan threshold governance |
| 5 | Probability belum terkalibrasi | Medium | Calibration gap | Model tidak dikalibrasi | Human reviewer salah menafsirkan score | Calibration dan reliability monitoring |
| 6 | Threshold default arbitrer | Medium | Slider default tanpa justifikasi | Tidak ada risk appetite/kapasitas | Prioritisasi tidak konsisten | Threshold policy berbasis risiko dan kapasitas |
| 7 | Aggregate metrics menutupi issue | Medium | ROC-AUC baik tetapi fairness bermasalah | Segment metrics tidak wajib | Bias tidak terlihat | Wajibkan segmented metrics |
| 8 | Tidak ada model card lengkap | Medium | Artifact `model_card` bernilai `None` | Dokumentasi lifecycle belum dibuat | Akuntabilitas rendah | Buat model card dan approval record |
| 9 | Tidak ada monitoring drift | Medium | Tidak ada modul drift | Operasional AI belum lengkap | Model menurun tanpa terdeteksi | Monitoring drift dan retraining trigger |
| 10 | Human review belum terdokumentasi | High | Aplikasi hanya menampilkan score | Workflow keputusan belum didefinisikan | Overreliance pada score | SOP human-in-the-loop |
| 11 | Audit trail perubahan data/model tidak memadai | Medium | Model pkl tanpa lineage lengkap | MLOps governance belum lengkap | Sulit rekonstruksi versi | Versioning dan change management |
