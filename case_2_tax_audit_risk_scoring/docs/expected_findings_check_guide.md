# Expected Findings dan Cara Mengecek

Dokumen ini untuk fasilitator. Jangan dibagikan kepada peserta sebelum sesi pembahasan.

## Tujuan Dokumen

Dokumen ini membantu fasilitator menilai temuan peserta pada AI Risk Scoring Pemeriksaan Pajak. Temuan dipisahkan menjadi dua kelompok:

- Temuan teknis: kelemahan yang dapat diuji langsung pada aplikasi, dataset, model, kode, atau dashboard.
- Temuan lifecycle/operasional: kelemahan pada tata kelola pengembangan model, deployment, monitoring, SDM, versioning, dan penggunaan score.

## Ringkasan Skenario

Aplikasi menghasilkan `Tax Audit Risk Score` 0-100% untuk prioritisasi review pemeriksaan pajak. Area yang perlu diperhatikan auditor mencakup data quality, threshold, fairness, explainability, label leakage, calibration, lifecycle governance, deployment, monitoring drift, dan human review.

## A. Expected Findings Teknis

| No | Expected Finding | Detail | Cara Mengecek | Evidence yang Diharapkan |
|---|---|---|---|---|
| T1 | Data quality issue | Dataset memiliki missing values, outlier omzet, dan kategori sektor tidak konsisten seperti `Perdagangan`, `perdagangan`, dan `Dagang`. | Buka `Data Audit`. Periksa missing values, kategori sektor, dan statistik `annual_revenue`. | Screenshot Data Audit, daftar missing, kategori tidak konsisten, dan outlier omzet. |
| T2 | Threshold default arbitrer | Threshold visual default 50% belum dikaitkan dengan risk appetite, kapasitas pemeriksaan, atau cost-benefit. | Buka `Performance & Threshold`, ubah threshold 35%, 50%, 65%, lalu bandingkan selected rate, precision, recall, dan F1-score. | Screenshot metrik pada beberapa threshold dan catatan trade-off. |
| T3 | Aggregate performance dapat menutupi isu fairness | ROC-AUC dan metrik agregat dapat terlihat cukup baik, tetapi performa antar kelompok berbeda. | Bandingkan metrik agregat dengan tabel per group di `Fairness`. | Screenshot performance dan fairness table. |
| T4 | Fairness gap pada demographic/segment group | Score, high-risk rate, FPR, atau FNR dapat berbeda antar Group A-D. | Buka `Fairness`, pilih `demographic_group`, catat average score, high-risk rate, FPR, dan FNR. | Tabel fairness per Group A-D. |
| T5 | Proxy bias pada wilayah/sektor/ukuran usaha | Perbedaan score/error rate dapat muncul pada `kpp_region`, `sector`, dan `business_size`. | Di menu `Fairness`, uji `sector`, `business_size`, dan `kpp_region`. | Screenshot tabel fairness untuk minimal dua atribut proxy. |
| T6 | Label leakage atau over-reliance pada skor historis | Fitur `leakage_previous_system_score` terlalu dekat dengan target dan berpengaruh besar. | Buka `SHAP Explainability`, periksa global feature importance dan kontribusi lokal. Review `utils/model_utils.py`. | Feature importance tinggi, grafik SHAP-style, dan kutipan kode. |
| T7 | Probability belum tentu terkalibrasi | Risk score ditampilkan sebagai probability, tetapi reliability check dapat menunjukkan gap predicted vs observed. | Buka `Performance & Threshold`, lihat reliability check. | Screenshot reliability table dengan calibration gap. |
| T8 | Explainability masih terbatas | Visualisasi SHAP-style berbasis perturbasi sederhana. Berguna untuk interpretasi awal, tetapi bukan validasi explainability penuh. | Buka `SHAP Explainability`, pilih taxpayer_id, lihat grafik kontribusi lokal. Review `utils/explainability_utils.py`. | Screenshot grafik SHAP-style dan catatan batasan metode. |

## B. Expected Findings Lifecycle/Operasional

| No | Expected Finding | Detail | Cara Mengecek | Evidence yang Diharapkan |
|---|---|---|---|---|
| L1 | Ketergantungan tinggi pada satu PIC data science | Satu PIC menangani data, training model, dashboard, dan deployment. Risiko continuity dan key-person dependency tinggi. | Review `docs/lifecycle_narrative.md`, bagian Identitas Sistem dan Pengembangan. | Kutipan narasi tentang satu PIC dan catatan risiko keberlanjutan. |
| L2 | Repository, versioning, dan release management belum rapi | Kode, dataset, dan model pernah dikelola di folder kerja bersama; belum ada branching, PR, release tag, atau issue tracking yang konsisten. | Review lifecycle narrative dan struktur repo. | Kutipan narasi dan daftar praktik version control yang belum ada. |
| L3 | Dokumentasi model belum lengkap | Belum ada model card formal, data dictionary final, feature eligibility register, dan acceptance criteria. | Review lifecycle narrative bagian Pengembangan, Data dan Fitur, Model dan Evaluasi. | Kutipan narasi dan daftar artefak model governance yang belum lengkap. |
| L4 | Independent model validation belum ada | Validasi awal dilakukan melalui metrik dan diskusi SME, belum ada validator independen. | Review lifecycle narrative bagian Pengembangan dan Model dan Evaluasi. | Catatan tidak adanya independent validation dan approval formal. |
| L5 | Deployment dan retraining masih manual | PIC menjalankan script training, menyimpan model, dan menjalankan Streamlit manual. | Review lifecycle narrative bagian Deployment. | Kutipan alur deployment/retraining manual. |
| L6 | Audit trail perubahan data, fitur, model, dan threshold belum memadai | Tidak ada hash artefak, training run id, metadata lineage, approval record, atau perbandingan formal antar versi. | Review `data/`, `models/`, `train_model.py`, README, dan lifecycle narrative. | Catatan gap MLOps dan tidak adanya metadata/versioning. |
| L7 | Monitoring drift belum tersedia | Belum ada input drift, score drift, calibration drift, fairness drift, performance drift, trigger retraining, atau alert. | Review lifecycle narrative bagian Operasi dan Monitoring. Cek menu aplikasi. | Kutipan narasi monitoring dan screenshot menu tanpa drift monitoring. |
| L8 | Human review belum tercatat di aplikasi | Score dinyatakan decision support, tetapi aplikasi tidak mencatat keputusan reviewer, override, approval supervisor, atau feedback untuk retraining. | Review lifecycle narrative bagian Penggunaan dan Human Review. Cek UI aplikasi. | Screenshot UI dan catatan tidak adanya form review/override. |
| L9 | Supply chain/dependency governance belum memadai | Library dan runtime dikelola oleh PIC; belum ada SBOM, vulnerability scan, policy update library, atau baseline konfigurasi server. | Review lifecycle narrative bagian Infrastruktur dan Dependensi. | Kutipan narasi dan daftar bukti yang belum tersedia. |

## Test Script Cepat Fasilitator

1. Jalankan `python train_model.py` lalu `streamlit run app.py`.
2. Buka `Overview`, catat jumlah data, rata-rata score, dan ROC-AUC.
3. Buka `Data Audit`, catat missing values, kategori sektor, dan outlier.
4. Buka `Performance & Threshold`, ambil evidence pada threshold 35%, 50%, dan 65%.
5. Buka `Fairness`, pilih `demographic_group`, `sector`, dan `kpp_region`.
6. Buka `SHAP Explainability`, pilih minimal dua taxpayer_id dengan score berbeda.
7. Review `docs/lifecycle_narrative.md`.
8. Review kode `utils/model_utils.py`, `utils/data_generator.py`, dan `utils/explainability_utils.py`.

## Kriteria Pembahasan

Peserta dianggap menemukan isu dengan baik jika mampu memisahkan:

- bukti teknis dari dashboard/dataset/kode; dan
- bukti lifecycle dari narasi pengembangan, deployment, monitoring, SDM, dan governance.

Temuan yang kuat perlu menjelaskan kondisi, kriteria, sebab, dampak, evidence, dan rekomendasi yang realistis untuk organisasi yang masih berada pada tahap awal tata kelola AI.
