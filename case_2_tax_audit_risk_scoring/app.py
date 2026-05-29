from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from train_model import train
from train_model import binary_metrics, roc_auc_score_simple
from utils.calibration_utils import calibration_table
from utils.data_generator import write_dataset
from utils.explainability_utils import global_feature_importance, local_perturbation_explanation, shap_like_contributions
from utils.fairness_utils import group_score_summary
from utils.model_utils import FEATURE_COLUMNS, load_artifact, risk_band, score_dataframe


BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "taxpayer_risk_dummy.csv"
MODEL_PATH = BASE_DIR / "models" / "taxpayer_risk_model.pkl"


def confusion_matrix_simple(y_true, y_pred) -> pd.DataFrame:
    tn = int(((y_true == 0) & (y_pred == 0)).sum())
    fp = int(((y_true == 0) & (y_pred == 1)).sum())
    fn = int(((y_true == 1) & (y_pred == 0)).sum())
    tp = int(((y_true == 1) & (y_pred == 1)).sum())
    return pd.DataFrame([[tn, fp], [fn, tp]], index=["Actual Low", "Actual High"], columns=["Pred Low", "Pred High"])

st.set_page_config(page_title="AI Risk Scoring Pemeriksaan Pajak", layout="wide", initial_sidebar_state="expanded")


@st.cache_data
def load_dataset() -> pd.DataFrame:
    if not DATA_PATH.exists():
        write_dataset(DATA_PATH)
    return pd.read_csv(DATA_PATH)


@st.cache_resource
def load_model_artifact() -> dict:
    if not MODEL_PATH.exists():
        train()
    return load_artifact(MODEL_PATH)


df = load_dataset()
artifact = load_model_artifact()
pipeline = artifact["pipeline"]
df_scored = df.copy()
df_scored["risk_score"] = score_dataframe(pipeline, df_scored)

st.title("AI Risk Scoring Pemeriksaan Pajak")
st.caption("Simulasi edukasi. Risk score adalah decision support 0-100%, bukan keputusan otomatis untuk menetapkan pemeriksaan.")

with st.sidebar:
    st.header("Pengaturan")
    threshold = st.slider("Threshold visual High Risk (%)", 10, 90, 50, 5)
    low_threshold = st.slider("Threshold visual Medium (%)", 5, threshold - 5, 35, 5)
    page = st.radio("Menu", ["Overview", "Prediksi", "Performance & Threshold", "Fairness", "SHAP Explainability", "Data Audit"])
    if st.button("Regenerate data dan retrain model"):
        write_dataset(DATA_PATH)
        train()
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()

if page == "Overview":
    st.subheader("Ringkasan Sistem")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Jumlah record", f"{len(df_scored):,}")
    c2.metric("Rata-rata risk score", f"{df_scored['risk_score'].mean():.1f}%")
    c3.metric("High risk rate", f"{(df_scored['risk_score'] >= threshold).mean():.1%}")
    c4.metric("ROC-AUC data uji saat training", f"{artifact['metrics']['roc_auc']:.3f}")
    st.write("Dataset sepenuhnya sintetis. Aplikasi menyediakan prediction, performance, threshold, fairness, explainability, dan data audit.")
    st.dataframe(df_scored.head(25), use_container_width=True, hide_index=True)

elif page == "Prediksi":
    st.subheader("Prediksi Single Input")
    sample = df_scored.iloc[0].to_dict()
    col1, col2, col3 = st.columns(3)
    with col1:
        taxpayer_type = st.selectbox("Jenis wajib pajak", ["Badan", "Orang Pribadi"])
        sector = st.selectbox("Sektor usaha", ["Perdagangan", "Jasa", "Manufaktur", "Konstruksi", "Transportasi", "Digital", "Dagang"])
        annual_revenue = st.number_input("Omzet tahunan", min_value=0.0, value=float(sample["annual_revenue"]), step=100_000_000.0)
        revenue_growth = st.number_input("Pertumbuhan omzet", value=float(sample["revenue_growth"]), step=0.01)
        tax_to_revenue_ratio = st.number_input("Rasio pajak terhadap omzet", value=float(sample["tax_to_revenue_ratio"] if pd.notna(sample["tax_to_revenue_ratio"]) else 0.05), step=0.005)
    with col2:
        late_filing_count = st.number_input("Keterlambatan pelaporan", min_value=0, value=int(sample["late_filing_count"]))
        correction_history_count = st.number_input("Histori koreksi", min_value=0, value=int(sample["correction_history_count"]))
        related_party_transactions = st.selectbox("Transaksi afiliasi", [0, 1], format_func=lambda x: "Ya" if x else "Tidak")
        kpp_region = st.selectbox("Lokasi/KPP", sorted(df["kpp_region"].dropna().unique()))
        pkp_status = st.selectbox("Status PKP", ["PKP", "Non-PKP"])
    with col3:
        business_size = st.selectbox("Ukuran usaha", ["Mikro", "Kecil", "Menengah", "Besar"])
        cash_transaction_ratio = st.number_input("Rasio transaksi tunai", value=float(sample["cash_transaction_ratio"]), step=0.01)
        e_invoice_mismatch_rate = st.number_input("Mismatch e-Faktur", value=float(sample["e_invoice_mismatch_rate"]), step=0.005)
        prior_audit_adjustment_amount = st.number_input("Nilai koreksi audit sebelumnya", min_value=0.0, value=float(sample["prior_audit_adjustment_amount"]), step=10_000_000.0)
        demographic_group = st.selectbox("Demographic group sintetis", ["Group A", "Group B", "Group C", "Group D"])
        leakage_previous_system_score = st.number_input("Skor sistem sebelumnya", min_value=0.0, max_value=100.0, value=float(sample["leakage_previous_system_score"]))

    input_df = pd.DataFrame([{"taxpayer_type": taxpayer_type, "sector": sector, "annual_revenue": annual_revenue, "revenue_growth": revenue_growth, "tax_to_revenue_ratio": tax_to_revenue_ratio, "late_filing_count": late_filing_count, "correction_history_count": correction_history_count, "related_party_transactions": related_party_transactions, "kpp_region": kpp_region, "pkp_status": pkp_status, "business_size": business_size, "cash_transaction_ratio": cash_transaction_ratio, "e_invoice_mismatch_rate": e_invoice_mismatch_rate, "prior_audit_adjustment_amount": prior_audit_adjustment_amount, "demographic_group": demographic_group, "leakage_previous_system_score": leakage_previous_system_score}])
    score = float(score_dataframe(pipeline, input_df).iloc[0])
    st.metric("Tax Audit Risk Score", f"{score:.1f}%", help="Probability score dari model, bukan keputusan otomatis.")
    st.write(f"Kategori visual: **{risk_band(score, low_threshold, threshold)}**")
    st.dataframe(input_df, use_container_width=True, hide_index=True)

elif page == "Performance & Threshold":
    st.subheader("Performance & Threshold")
    y_true = df_scored["audit_risk_label"].astype(int)
    y_prob = df_scored["risk_score"] / 100
    y_pred = (df_scored["risk_score"] >= threshold).astype(int)
    metrics = binary_metrics(y_true.to_numpy(), y_prob.to_numpy(), threshold / 100)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("ROC-AUC", f"{roc_auc_score_simple(y_true.to_numpy(), y_prob.to_numpy()):.3f}")
    c2.metric("Precision", f"{metrics['precision']:.3f}")
    c3.metric("Recall", f"{metrics['recall']:.3f}")
    c4.metric("F1-score", f"{metrics['f1']:.3f}")
    st.dataframe(confusion_matrix_simple(y_true, y_pred), use_container_width=True)
    st.write("Reliability check sederhana.")
    st.dataframe(calibration_table(y_true, y_prob), use_container_width=True, hide_index=True)

    st.write("Analisis threshold ringkas.")
    rows = []
    for t in range(20, 86, 5):
        y_pred = (df_scored["risk_score"] >= t).astype(int)
        metrics = binary_metrics(y_true.to_numpy(), (df_scored["risk_score"] / 100).to_numpy(), t / 100)
        rows.append({"threshold_percent": t, "selected_rate": round(y_pred.mean(), 3), "precision": round(metrics["precision"], 3), "recall": round(metrics["recall"], 3), "f1_score": round(metrics["f1"], 3)})
    threshold_df = pd.DataFrame(rows)
    st.dataframe(threshold_df, use_container_width=True, hide_index=True)
    st.line_chart(threshold_df.set_index("threshold_percent")[["precision", "recall", "f1_score"]])

elif page == "Fairness":
    st.subheader("Fairness Audit")
    group_col = st.selectbox("Analisis berdasarkan atribut", ["sector", "business_size", "kpp_region", "demographic_group", "taxpayer_type", "pkp_status"])
    summary = group_score_summary(df_scored, group_col, "risk_score", threshold, label_col="audit_risk_label")
    st.dataframe(summary, use_container_width=True, hide_index=True)
    st.bar_chart(summary.set_index("group")[["average_score", "high_risk_rate_by_threshold"]])

elif page == "SHAP Explainability":
    st.subheader("SHAP Explainability")
    importance = global_feature_importance(pipeline)
    st.write("Global feature importance sederhana.")
    st.dataframe(importance, use_container_width=True, hide_index=True)
    st.bar_chart(importance.set_index("feature")["importance"])
    taxpayer_id = st.selectbox("Pilih taxpayer_id", df_scored["taxpayer_id"].head(250))
    selected_row = df_scored.loc[df_scored["taxpayer_id"] == taxpayer_id, FEATURE_COLUMNS]
    selected_score = float(score_dataframe(pipeline, selected_row).iloc[0])
    st.metric("Risk score record terpilih", f"{selected_score:.1f}%")
    shap_df = shap_like_contributions(pipeline, selected_row, df_scored[FEATURE_COLUMNS]).head(12)
    st.write("Visualisasi SHAP-style: nilai positif menaikkan risk score, nilai negatif menurunkan risk score.")
    st.bar_chart(shap_df.set_index("feature")["shap_value"])
    st.dataframe(shap_df, use_container_width=True, hide_index=True)
    with st.expander("Detail local perturbation"):
        st.dataframe(local_perturbation_explanation(pipeline, selected_row, df_scored[FEATURE_COLUMNS]), use_container_width=True, hide_index=True)

elif page == "Data Audit":
    st.subheader("Data Audit")
    missing = df.isna().sum().reset_index()
    missing.columns = ["column", "missing_count"]
    missing["missing_rate"] = (missing["missing_count"] / len(df)).round(3)
    st.dataframe(missing, use_container_width=True, hide_index=True)
    c1, c2 = st.columns(2)
    with c1:
        st.write("Distribusi label dummy")
        st.dataframe(df["audit_risk_label"].value_counts(normalize=True).rename("rate").reset_index(), hide_index=True)
    with c2:
        st.write("Kategori sektor")
        st.dataframe(df["sector"].value_counts(dropna=False).reset_index(), hide_index=True)
    st.write("Statistik numerik")
    st.dataframe(df.select_dtypes(include="number").describe().T, use_container_width=True)
