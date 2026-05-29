# Studi Kasus 2: AI Risk Scoring Pemeriksaan Pajak

Dokumen fasilitator. Jangan dibagikan langsung kepada peserta.

## Background Kasus

Direktorat Analitika Kepatuhan mengembangkan sistem AI untuk memberi `Tax Audit Risk Score` kepada wajib pajak. Score digunakan sebagai decision support untuk membantu prioritisasi analisis risiko, bukan keputusan otomatis untuk menetapkan pemeriksaan.

Dalam narasi pemilik sistem, aplikasi masih berada pada tahap inisiasi/pilot analitik internal. Tata kelola pengembangan model belum matang: masih bergantung pada satu PIC data science, dokumentasi model belum lengkap, repository/versioning belum rapi, deployment dan retraining dilakukan manual, monitoring drift belum tersedia, dan audit trail perubahan model/data belum memadai.

## Tujuan Sistem dan Batasan Penggunaan

- Menghasilkan probability score 0-100%.
- Menampilkan Low/Medium/High hanya sebagai visualisasi threshold.
- Mendukung review manusia dan analisis risiko lanjutan.
- Tidak boleh digunakan sebagai automated decision tanpa validasi kebijakan, hukum, dan tata kelola.

## Dataset

Dataset `data/taxpayer_risk_dummy.csv` memuat sektor, omzet, pertumbuhan omzet, rasio pajak terhadap omzet, keterlambatan pelaporan, histori koreksi, transaksi afiliasi, lokasi/KPP, status PKP, ukuran usaha, indikator risiko, `demographic_group` Group A-D, target probability, dan label evaluasi.

`demographic_group` digunakan untuk fairness testing. Label tersebut netral dan tidak merepresentasikan kelompok masyarakat tertentu.

## Model dan Risk Scoring

`train_model.py` membuat model simulasi lokal berbasis `numpy/pandas` dengan metode `predict_proba`. Model mempelajari baseline rate dan risk rate per kategori dari data training, lalu menggabungkannya dengan sinyal numerik untuk menghasilkan risk score 0-100%. Aplikasi disederhanakan menjadi menu inti dan menyediakan visualisasi SHAP-style untuk menjelaskan kontribusi lokal setiap fitur terhadap score.

## Kondisi Lifecycle/Operasional

Lihat `docs/lifecycle_narrative.md` sebagai artefak asesmen. Area yang sengaja dibuat realistis untuk dinilai auditor:

- ketergantungan tinggi pada satu PIC data science;
- dokumentasi model, data dictionary, dan feature eligibility belum lengkap;
- repository, branching, reviewer independen, release tag, dan issue tracking belum rapi;
- deployment dan retraining manual tanpa model registry, approval, rollback, dan metadata lineage yang konsisten;
- audit trail perubahan dataset, fitur, model, dan threshold belum memadai;
- monitoring input drift, score drift, calibration drift, fairness drift, dan performance drift belum tersedia;
- human review dan override belum tercatat di aplikasi.

## Kelemahan yang Sengaja Ditanamkan

### Teknis

- Dataset imbalance pada threshold tertentu.
- Bias/proxy bias pada sektor, wilayah/KPP, ukuran usaha, dan atribut demografis sintetis.
- Bias sintetis terhadap `Group C`.
- Data quality issue: missing values, outlier omzet, dan kategori sektor tidak konsisten.
- Label leakage melalui `leakage_previous_system_score`.
- Model over-reliance pada fitur yang tidak semestinya.
- Aggregate performance menutupi fairness issue.
- Probability score belum dikalibrasi dengan baik.
- Threshold default arbitrer.
- Tidak ada model card, monitoring drift, documented human review, policy atribut sensitif/proxy, dan audit trail memadai.

### Lifecycle/Operasional

- Ketergantungan tinggi pada satu PIC data science.
- Repository, versioning, dan release management belum rapi.
- Model card, data dictionary, feature eligibility, dan acceptance criteria belum lengkap.
- Independent model validation belum tersedia.
- Deployment, retraining, dan rollback masih manual.
- Monitoring drift dan audit trail perubahan model/data belum memadai.

## Audit Objectives

Menilai kualitas data, balancing, lifecycle, performance, calibration, threshold, fairness, explainability, human-in-the-loop, model card, monitoring, audit evidence, deployment, retraining, SDM/PIC, dan change management.

## Suggested Audit Procedures

- Review dataset, training script, dan fitur.
- Jalankan data audit untuk missing, outlier, inconsistent category.
- Uji ROC-AUC, precision, recall, F1-score, dan confusion matrix pada threshold 35%, 50%, 65%.
- Review calibration table.
- Uji fairness pada `sector`, `business_size`, `kpp_region`, dan `demographic_group`.
- Review feature importance dan visualisasi SHAP-style local contribution.
- Cari model card, drift monitoring, approval, human review, dan audit trail.
- Review `docs/lifecycle_narrative.md` untuk menilai PIC, repository/versioning, deployment, retraining, monitoring drift, human review, dan audit trail perubahan model/data.

## Test Cases

- Data quality: missing value, outlier `annual_revenue`, kategori `sector`.
- Imbalance: distribusi label dan selected rate.
- Bias/fairness: average score, high-risk rate, FPR, FNR per group.
- Explainability: global importance dan local explanation.
- Performance/calibration: ROC-AUC, precision, recall, F1, reliability table.
- Governance: model card, monitoring drift, human review, change management.
- Lifecycle: PIC, repository/versioning, deployment manual, retraining manual, audit trail model/data, dan monitoring drift.

## Expected Findings

### Teknis

- Ada missing value, outlier, dan inconsistent category.
- `leakage_previous_system_score` terlalu dekat dengan target.
- Score dan error rate berbeda antar group, termasuk `demographic_group`.
- ROC-AUC aggregate terlihat baik tetapi fairness/calibration issue tetap ada.
- Threshold default tidak didukung justifikasi risiko atau kapasitas.
- Tidak ada model card, drift monitoring, human review procedure, dan audit trail.

### Lifecycle/Operasional

- Ketergantungan pada satu PIC data science.
- Repository, release management, dan review independen belum memadai.
- Model card, data dictionary, feature eligibility, dan acceptance criteria belum lengkap.
- Deployment/retraining manual dan belum memiliki approval/rollback formal.
- Monitoring drift belum tersedia.
- Human review dan override belum tercatat di aplikasi.

## Rekomendasi Kontrol

Buat data quality rules, hapus/justifikasi fitur leakage, lakukan fairness assessment berkala, kalibrasi probability, tetapkan threshold berbasis risk appetite dan kapasitas, buat model card, human review SOP, monitoring drift, retraining governance, audit trail, dan policy penggunaan atribut sensitif/proxy.
