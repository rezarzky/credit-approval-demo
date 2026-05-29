# Panduan Audit Fasilitator: AI Risk Scoring Pemeriksaan Pajak

## Setup

```bash
cd case_2_tax_audit_risk_scoring
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Audit Procedures Detail

1. Review tujuan dan batasan: pastikan score dipahami sebagai decision support.
2. Data quality: buka `Data Audit`, catat missing values, outlier, dan kategori tidak konsisten.
3. Model performance: buka `Performance & Threshold`, ubah threshold, dan catat precision, recall, F1-score, confusion matrix.
4. Calibration: review reliability check dan gap predicted probability vs observed rate.
5. Threshold analysis: gunakan tabel threshold pada halaman yang sama untuk mendiskusikan selected rate, kapasitas pemeriksaan, dan risk appetite.
6. Fairness: buka `Fairness`, uji `sector`, `business_size`, `kpp_region`, dan `demographic_group`.
7. Explainability: buka `SHAP Explainability`, review feature importance dan visualisasi SHAP-style local contribution.
8. Governance: review model card, drift monitoring, human review, dan audit trail.

## Test Script

1. Catat ROC-AUC overview.
2. Threshold 50%: ambil confusion matrix dan fairness `demographic_group`.
3. Threshold 35% dan 65%: bandingkan precision, recall, selected rate.
4. Buka `Data Audit` dan catat missing/outlier/kategori.
5. Buka `SHAP Explainability`, cek feature importance dan grafik kontribusi lokal.
6. Review `train_model.py` dan `utils/data_generator.py`.

## Kriteria Penilaian

- Identifikasi issue data/model/fairness: 30%.
- Kualitas evidence: 25%.
- Analisis dampak terhadap SPBE dan pemeriksaan: 20%.
- Rekomendasi kontrol realistis: 20%.
- Struktur laporan: 5%.

## Expected Evidence

Screenshot Overview, Data Audit, Performance & Threshold pada minimal dua threshold, fairness untuk `demographic_group` dan satu atribut lain, SHAP Explainability, kutipan kode, dan daftar artefak governance yang belum tersedia.

## Expected Findings

Data quality issue; label leakage/over-reliance pada `leakage_previous_system_score`; fairness gap pada atribut sintetis dan proxy; probability belum terkalibrasi; threshold arbitrer; tidak ada model card, monitoring drift, human review SOP, dan audit trail perubahan model/data.

## Rekomendasi Kontrol

Data quality checks, feature eligibility review, fairness assessment periodik, calibration/reliability monitoring, threshold policy, human review wajib, model card, retraining policy, dan versioning data/model.
