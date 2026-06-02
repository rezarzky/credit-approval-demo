# Expected Findings Check Guide - Case 2 Tax Audit Risk Scoring

File ini dipakai fasilitator untuk mengecek apakah peserta menemukan kelemahan utama yang sengaja ditanam pada aplikasi Streamlit case 2.

## Ringkasan Hasil yang Diharapkan

Peserta seharusnya melihat bahwa aplikasi risk scoring pajak:

- menghasilkan gap fairness yang mencolok pada `demographic_group`, terutama `Group C`;
- menggunakan `leakage_previous_system_score` sebagai fitur yang terlalu dominan dan berisiko menjadi data leakage;
- menampilkan penjelasan lokal SHAP-style langsung di bawah hasil prediksi single input;
- memiliki masalah kualitas data seperti nilai kosong, kategori tidak konsisten, dan outlier;
- belum menunjukkan governance control yang cukup untuk threshold, model monitoring, validasi data, dan human-in-the-loop.

## Check Guide per Menu

### 1. Prediksi

Hal yang perlu dicek:

- Ubah `demographic_group` dari `Group A` atau `Group B` ke `Group C` dengan input lain tetap sama.
- Risk score seharusnya naik secara terlihat.
- Bagian `Faktor Utama Prediksi` muncul langsung di bawah hasil skor.
- `demographic_group` dan/atau `leakage_previous_system_score` dapat muncul sebagai kontributor besar pada tabel SHAP-style.
- Tabel sensitivitas menunjukkan perubahan skor ketika hanya `demographic_group` diganti.

Expected finding:

- Peserta menyimpulkan ada risiko penggunaan atribut sensitif/sintetis atau proxy dalam keputusan risk scoring.
- Peserta menyimpulkan explainability membantu mendeteksi faktor yang tidak semestinya terlalu berpengaruh.

### 2. Fairness

Hal yang perlu dicek:

- Pilih atribut `demographic_group`.
- Perhatikan metric `Gap selection rate`.
- `Group C` seharusnya memiliki `average_score` dan `high_risk_rate_by_threshold` jauh lebih tinggi dibanding sebagian besar grup lain.

Expected finding:

- Ada indikasi disparate impact atau perbedaan treatment berbasis grup.
- Auditor perlu meminta justifikasi bisnis, uji fairness pra-produksi, dokumentasi fitur, dan mekanisme mitigasi.
- Threshold tunggal dapat menyebabkan beban pemeriksaan yang tidak proporsional pada grup tertentu.

### 3. Performance & Threshold

Hal yang perlu dicek:

- Ubah threshold visual high risk.
- Amati perubahan precision, recall, F1, dan selected rate.

Expected finding:

- Threshold belum cukup jika hanya dipilih dari metrik agregat.
- Threshold perlu dievaluasi bersama biaya false positive, false negative, kapasitas pemeriksaan, fairness per grup, dan prosedur eskalasi manual.

### 4. Data Audit

Hal yang perlu dicek:

- `tax_to_revenue_ratio` memiliki missing value.
- `sector` memiliki missing value dan kategori tidak konsisten seperti `perdagangan` dan `Dagang`.
- `annual_revenue` memiliki outlier sintetis.

Expected finding:

- Perlu kontrol data quality sebelum scoring.
- Perlu definisi data owner, validasi skema, standardisasi kategori, treatment missing value, dan monitoring drift.

### 5. Overview

Hal yang perlu dicek:

- Aplikasi menyatakan dataset sintetis dan risk score hanya decision support.
- Namun belum ada model card lengkap, approval workflow, audit trail, dan dokumentasi monitoring.

Expected finding:

- Sistem belum siap dinilai sebagai sistem operasional penuh.
- Perlu tata kelola model, data, keamanan, monitoring, dan human-in-the-loop sebelum digunakan pada proses nyata.

## Daftar Temuan Minimal yang Diharapkan dari Peserta

1. Bias/fairness: `Group C` lebih sering diprediksi high risk.
2. Explainability: faktor lokal menunjukkan atribut grup/proxy dapat memengaruhi skor.
3. Data leakage: `leakage_previous_system_score` terlalu dominan dan berpotensi membawa bias historis.
4. Data quality: missing value, kategori tidak konsisten, dan outlier belum ditangani memadai.
5. Threshold governance: threshold perlu dasar kebijakan dan evaluasi dampak.
6. Human oversight: skor belum boleh menjadi keputusan otomatis tanpa review petugas.
7. Monitoring: perlu pemantauan model drift, data drift, fairness drift, dan performa pasca-implementasi.
8. Documentation: perlu model card, data sheet, risk assessment, dan eviden validasi.

## Contoh Kesimpulan Peserta yang Baik

Model dapat digunakan sebagai alat bantu prioritisasi hanya jika dilengkapi validasi data, uji fairness, justifikasi fitur, monitoring berkala, dan mekanisme review manusia. Dalam kondisi demo ini, ada indikasi kuat bahwa model mempelajari pola historis yang bias, terutama dari `demographic_group` dan `leakage_previous_system_score`, sehingga belum layak digunakan sebagai dasar otomatis penetapan pemeriksaan.
