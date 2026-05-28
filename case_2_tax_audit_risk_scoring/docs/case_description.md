# Studi Kasus 2: AI Risk Scoring Pemeriksaan Pajak

Dokumen fasilitator. Jangan dibagikan langsung kepada peserta.

## Background Kasus

Direktorat Analitika Kepatuhan, unit fiktif untuk pelatihan, mengembangkan sistem AI untuk memberi `Tax Audit Risk Score` kepada wajib pajak. Score digunakan sebagai decision support untuk membantu prioritisasi analisis risiko, bukan keputusan otomatis untuk menetapkan pemeriksaan.

Dataset, label, model, dan atribut demografis sepenuhnya sintetis.

## Tujuan Sistem dan Batasan Penggunaan

- Menghasilkan probability score 0-100%.
- Menampilkan Low/Medium/High hanya sebagai visualisasi threshold.
- Mendukung review manusia dan analisis risiko lanjutan.
- Tidak boleh digunakan sebagai automated decision tanpa validasi kebijakan, hukum, dan tata kelola.

## Dataset Dummy

Dataset `data/taxpayer_risk_dummy.csv` memuat sektor, omzet, pertumbuhan omzet, rasio pajak terhadap omzet, keterlambatan pelaporan, histori koreksi, transaksi afiliasi, lokasi/KPP, status PKP, ukuran usaha, indikator risiko, `demographic_group` sintetis Group A-D, target probability dummy, dan label dummy.

`demographic_group` hanya untuk pembelajaran fairness testing. Label tersebut bukan data nyata dan tidak merepresentasikan kelompok masyarakat.

## Model dan Risk Scoring

`train_model.py` membuat model simulasi lokal berbasis `numpy/pandas` dengan metode `predict_proba`. Model mempelajari baseline rate dan risk rate per kategori dari data training, lalu menggabungkannya dengan sinyal numerik untuk menghasilkan risk score 0-100%. Pendekatan ini sengaja ringan agar mudah dijalankan di kelas tanpa API eksternal atau dependensi ML berat.

## Kelemahan yang Sengaja Ditanamkan

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

## Audit Objectives

Menilai kualitas data, balancing, lifecycle, performance, calibration, threshold, fairness, explainability, human-in-the-loop, model card, monitoring, dan audit evidence.

## Suggested Audit Procedures

- Review dataset, training script, dan fitur.
- Jalankan data audit untuk missing, outlier, inconsistent category.
- Uji ROC-AUC, precision, recall, F1-score, dan confusion matrix pada threshold 35%, 50%, 65%.
- Review calibration table.
- Uji fairness pada `sector`, `business_size`, `kpp_region`, dan `demographic_group`.
- Review feature importance dan local perturbation explanation.
- Cari model card, drift monitoring, approval, human review, dan audit trail.

## Test Cases

- Data quality: missing value, outlier `annual_revenue`, kategori `sector`.
- Imbalance: distribusi label dan selected rate.
- Bias/fairness: average score, high-risk rate, FPR, FNR per group.
- Explainability: global importance dan local explanation.
- Performance/calibration: ROC-AUC, precision, recall, F1, reliability table.
- Governance: model card, monitoring drift, human review, change management.

## Expected Findings

- Ada missing value, outlier, dan inconsistent category.
- `leakage_previous_system_score` terlalu dekat dengan target.
- Score dan error rate berbeda antar group, termasuk `demographic_group`.
- ROC-AUC aggregate terlihat baik tetapi fairness/calibration issue tetap ada.
- Threshold default tidak didukung justifikasi risiko atau kapasitas.
- Tidak ada model card, drift monitoring, human review procedure, dan audit trail.

## Rekomendasi Kontrol

Buat data quality rules, hapus/justifikasi fitur leakage, lakukan fairness assessment berkala, kalibrasi probability, tetapkan threshold berbasis risk appetite dan kapasitas, buat model card, human review SOP, monitoring drift, retraining governance, audit trail, dan policy penggunaan atribut sensitif/proxy.
