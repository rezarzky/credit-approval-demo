# Expected Findings dan Cara Mengecek

Dokumen ini untuk fasilitator. Jangan dibagikan kepada peserta sebelum sesi pembahasan.

## Tujuan Dokumen

Dokumen ini membantu fasilitator menilai apakah peserta berhasil menemukan kelemahan utama pada aplikasi AI Risk Scoring Pemeriksaan Pajak. Setiap temuan dilengkapi detail, cara mengecek, dan evidence yang diharapkan.

## Ringkasan Skenario

Aplikasi menghasilkan `Tax Audit Risk Score` 0-100% untuk simulasi prioritisasi review pemeriksaan pajak. Sistem sengaja dibuat sederhana dan memiliki isu data quality, threshold, fairness, explainability, label leakage, calibration, dan governance.

## Daftar Expected Findings

| No | Expected Finding | Detail | Cara Mengecek | Evidence yang Diharapkan |
|---|---|---|---|---|
| 1 | Data quality issue | Dataset memiliki missing values, outlier omzet, dan kategori sektor tidak konsisten seperti `Perdagangan`, `perdagangan`, dan `Dagang`. | Buka menu `Data Audit`. Periksa tabel missing values, kategori sektor, dan statistik numerik `annual_revenue`. | Screenshot Data Audit, daftar kolom missing, kategori sektor tidak konsisten, dan outlier omzet. |
| 2 | Threshold default arbitrer | Threshold visual default 50% belum dikaitkan dengan risk appetite, kapasitas pemeriksaan, atau cost-benefit. | Buka `Performance & Threshold`, ubah threshold 35%, 50%, 65%, lalu bandingkan selected rate, precision, recall, dan F1-score. | Screenshot metrik pada beberapa threshold dan catatan trade-off. |
| 3 | Aggregate performance dapat menutupi isu fairness | ROC-AUC dan metrik agregat dapat terlihat cukup baik, tetapi performa antar kelompok berbeda. | Bandingkan metrik agregat di `Performance & Threshold` dengan tabel per group di `Fairness`. | Screenshot ROC-AUC/precision/recall serta tabel fairness yang menunjukkan perbedaan antar group. |
| 4 | Fairness gap pada demographic group sintetis | `demographic_group` adalah atribut sintetis untuk pengujian fairness. Score, high-risk rate, FPR, atau FNR dapat berbeda antar Group A-D. | Buka `Fairness`, pilih `demographic_group`, catat average score, high-risk rate, false positive rate, dan false negative rate. | Tabel fairness per Group A-D. |
| 5 | Proxy bias pada wilayah/sektor/ukuran usaha | Perbedaan score/error rate dapat muncul pada `kpp_region`, `sector`, dan `business_size`. | Di menu `Fairness`, uji `sector`, `business_size`, dan `kpp_region`. Bandingkan average score dan error rate. | Screenshot tabel fairness untuk minimal dua atribut proxy. |
| 6 | Label leakage atau over-reliance pada skor historis | Fitur `leakage_previous_system_score` terlalu dekat dengan target dan diberi pengaruh besar dalam model simulasi. | Buka `SHAP Explainability`, periksa global feature importance. Pilih beberapa taxpayer_id dan lihat kontribusi lokal. Review `utils/model_utils.py`. | Feature importance tinggi untuk `leakage_previous_system_score`, grafik SHAP-style, dan kutipan kode. |
| 7 | Probability belum tentu terkalibrasi | Risk score ditampilkan sebagai probability, tetapi reliability check dapat menunjukkan gap antara predicted probability dan observed rate. | Buka `Performance & Threshold`, lihat tabel reliability check. Bandingkan `avg_predicted_probability`, `observed_rate`, dan `calibration_gap`. | Screenshot reliability table dengan calibration gap. |
| 8 | Explainability masih terbatas | Visualisasi SHAP-style berbasis perturbasi sederhana, bukan SHAP library penuh. Ini berguna untuk kelas, tetapi perlu dijelaskan sebagai approximate explanation. | Buka `SHAP Explainability`, pilih taxpayer_id, lihat grafik kontribusi lokal dan tabel `shap_value`. Review `utils/explainability_utils.py`. | Screenshot grafik SHAP-style dan catatan batasan metode. |
| 9 | Human review belum terdokumentasi | Aplikasi menekankan decision support, tetapi belum ada workflow formal untuk review, approval, override, atau catatan alasan keputusan manusia. | Review UI dan dokumen/kode. Cari fitur maker-checker, komentar reviewer, approval, atau escalation. | Catatan absence of control dan screenshot UI yang hanya menampilkan score. |
| 10 | Model card belum lengkap | Artifact model berisi `model_card: None` dan belum ada dokumen formal model card operasional. | Review `train_model.py` dan file model artifact secara konseptual. Cek dokumen di folder `docs/`. | Kutipan `model_card: None` dari kode dan daftar elemen model card yang belum ada. |
| 11 | Drift monitoring belum tersedia | Aplikasi tidak memiliki monitoring input drift, performance drift, fairness drift, atau trigger retraining. | Review folder `utils/`, `app.py`, dan dokumen. Cari modul drift monitoring atau dashboard drift. | Catatan tidak adanya modul/fitur drift monitoring. |
| 12 | Audit trail perubahan data/model belum memadai | Tidak ada versioning dataset/model, hash, approval record, training run id, atau deployment log yang memadai. | Review `data/`, `models/`, `train_model.py`, dan README. Cek apakah ada metadata lineage. | Catatan gap MLOps/LLMOps governance dan daftar metadata yang belum tersedia. |

## Test Script Cepat untuk Fasilitator

1. Jalankan `python train_model.py` lalu `streamlit run app.py`.
2. Buka `Overview`, catat jumlah data, rata-rata score, dan ROC-AUC.
3. Buka `Data Audit`, catat missing values, kategori sektor, dan outlier.
4. Buka `Performance & Threshold`, ambil evidence pada threshold 35%, 50%, dan 65%.
5. Buka `Fairness`, pilih `demographic_group`, `sector`, dan `kpp_region`.
6. Buka `SHAP Explainability`, pilih minimal dua taxpayer_id dengan score berbeda.
7. Review kode `utils/model_utils.py`, `utils/data_generator.py`, dan `utils/explainability_utils.py`.
8. Susun pembahasan: data quality, leakage, fairness, calibration, threshold, explainability, dan governance.

## Kriteria Pembahasan

Peserta dianggap menemukan isu dengan baik jika mampu menunjukkan:

- evidence kuantitatif dari dashboard;
- evidence kode untuk fitur atau desain yang berisiko;
- perbedaan antara performance agregat dan fairness segment;
- batasan interpretasi risk score sebagai probability;
- rekomendasi yang tetap menjaga prinsip decision support dan human review.

## Rekomendasi Pembanding

Rekomendasi yang diharapkan muncul:

- data quality rules dan data validation sebelum training/scoring;
- standardisasi kategori dan treatment outlier;
- review feature eligibility untuk mencegah leakage/proxy bias;
- fairness testing berkala pada atribut sensitif/proxy;
- calibration atau reliability monitoring untuk probability score;
- threshold policy berbasis risk appetite, kapasitas, dan cost-benefit;
- model card lengkap;
- human review workflow dan dokumentasi override;
- drift monitoring dan retraining governance;
- audit trail data/model dengan versioning, hash, approval, dan training run metadata.
