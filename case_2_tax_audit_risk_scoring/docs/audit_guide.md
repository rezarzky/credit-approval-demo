# Panduan Audit Fasilitator: AI Risk Scoring Pemeriksaan Pajak

## Setup

```bash
cd case_2_tax_audit_risk_scoring
pip install -r requirements.txt
python train_model.py
streamlit run app.py
```

## Audit Procedures Detail

### Prosedur Teknis

1. Review tujuan dan batasan: pastikan score dipahami sebagai decision support.
2. Data quality: buka `Data Audit`, catat missing values, outlier, dan kategori tidak konsisten.
3. Model performance: buka `Performance & Threshold`, ubah threshold, dan catat precision, recall, F1-score, confusion matrix.
4. Calibration: review reliability check dan gap predicted probability vs observed rate.
5. Threshold analysis: gunakan tabel threshold pada halaman yang sama untuk mendiskusikan selected rate, kapasitas pemeriksaan, dan risk appetite.
6. Fairness: buka `Fairness`, uji `sector`, `business_size`, `kpp_region`, dan `demographic_group`.
7. Explainability: buka `SHAP Explainability`, review feature importance dan visualisasi SHAP-style local contribution.
8. Governance teknis: review model card, fairness assessment, calibration, human review, dan audit trail.

### Prosedur Lifecycle/Operasional

1. Review `docs/lifecycle_narrative.md`.
2. Identifikasi ketergantungan pada satu PIC dan kecukupan backup/transfer knowledge.
3. Nilai repository, branching, reviewer independen, release tag, dan issue tracking.
4. Nilai deployment/retraining manual: approval, rollback, model registry, metadata lineage, dan environment separation.
5. Nilai monitoring drift: input drift, score drift, calibration drift, fairness drift, performance drift, alert, dan trigger retraining.
6. Nilai human review: apakah keputusan reviewer, override, approval supervisor, dan feedback model tercatat.

## Test Script

1. Catat ROC-AUC overview.
2. Threshold 50%: ambil confusion matrix dan fairness `demographic_group`.
3. Threshold 35% dan 65%: bandingkan precision, recall, selected rate.
4. Buka `Data Audit` dan catat missing/outlier/kategori.
5. Buka `SHAP Explainability`, cek feature importance dan grafik kontribusi lokal.
6. Review `train_model.py` dan `utils/data_generator.py`.
7. Review lifecycle narrative dan kelompokkan temuan lifecycle terpisah dari temuan teknis.

## Kriteria Penilaian

- Identifikasi issue data/model/fairness: 30%.
- Kualitas evidence: 25%.
- Analisis dampak terhadap SPBE dan pemeriksaan: 20%.
- Rekomendasi kontrol realistis: 20%.
- Struktur laporan: 5%.

Laporan peserta sebaiknya memisahkan temuan teknis dan temuan lifecycle/operasional.

## Expected Evidence

Screenshot Overview, Data Audit, Performance & Threshold pada minimal dua threshold, fairness untuk `demographic_group` dan satu atribut lain, SHAP Explainability, kutipan kode, serta kutipan lifecycle narrative terkait PIC, repository, deployment, retraining, monitoring drift, human review, dan audit trail.

## Expected Findings

Teknis: data quality issue; label leakage/over-reliance pada `leakage_previous_system_score`; fairness gap pada atribut/proxy; probability belum terkalibrasi; threshold arbitrer.

Lifecycle/operasional: ketergantungan pada satu PIC data science; repository/versioning belum rapi; model card dan data dictionary belum lengkap; independent model validation belum ada; deployment/retraining manual; monitoring drift belum tersedia; human review dan audit trail perubahan model/data belum memadai.

## Rekomendasi Kontrol

Data quality checks, feature eligibility review, fairness assessment periodik, calibration/reliability monitoring, threshold policy, human review wajib, model card, retraining policy, dan versioning data/model. Untuk lifecycle, perkuat repository resmi, review independen, model registry, deployment approval, rollback, metadata lineage, monitoring drift, dan backup PIC.
