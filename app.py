import streamlit as st
import pandas as pd
import pickle
import shap
import numpy as np
import matplotlib.pyplot as plt
from pandas.api.types import is_object_dtype, is_string_dtype

# --- 1. Page Configuration ---
st.set_page_config(
    page_title="Simulasi Audit AI - Persetujuan Kredit",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. Load Artifacts ---
@st.cache_data
def load_data():
    """Loads the source dataset for SHAP background and fairness testing."""
    try:
        return pd.read_csv('credit_approval_biased_dataset.csv')
    except FileNotFoundError:
        return None


def build_fairness_summary(df, model_pipeline, label_encoder, group_col):
    """Build group-level fairness metrics for the approval decision."""
    scored_df = df.copy()
    feature_df = scored_df.drop('Keputusan', axis=1)
    scored_df["Prediksi_Model"] = label_encoder.inverse_transform(
        model_pipeline.predict(feature_df)
    )
    scored_df["Actual_Approved"] = (scored_df["Keputusan"] == "Disetujui").astype(int)
    scored_df["Predicted_Approved"] = (scored_df["Prediksi_Model"] == "Disetujui").astype(int)

    rows = []
    for group_value, group_df in scored_df.groupby(group_col, dropna=False):
        actual = group_df["Actual_Approved"]
        pred = group_df["Predicted_Approved"]
        false_approval = int(((actual == 0) & (pred == 1)).sum())
        true_rejection = int(((actual == 0) & (pred == 0)).sum())
        false_rejection = int(((actual == 1) & (pred == 0)).sum())
        true_approval = int(((actual == 1) & (pred == 1)).sum())

        rows.append({
            "Grup": group_value,
            "Jumlah": len(group_df),
            "Approval Rate Aktual": actual.mean(),
            "Approval Rate Model": pred.mean(),
            "False Approval Rate": false_approval / (false_approval + true_rejection) if (false_approval + true_rejection) else None,
            "False Rejection Rate": false_rejection / (false_rejection + true_approval) if (false_rejection + true_approval) else None,
            "Akurasi": (actual == pred).mean(),
        })

    summary = pd.DataFrame(rows).sort_values("Approval Rate Model", ascending=False)
    max_rate = summary["Approval Rate Model"].max()
    summary["Disparate Impact Ratio"] = summary["Approval Rate Model"].apply(
        lambda rate: rate / max_rate if max_rate else None
    )
    return summary


def fairness_flags(summary):
    """Create simple audit flags for classroom discussion, not legal conclusions."""
    approval_gap = summary["Approval Rate Model"].max() - summary["Approval Rate Model"].min()
    min_di = summary["Disparate Impact Ratio"].min()
    frr_gap = summary["False Rejection Rate"].max() - summary["False Rejection Rate"].min()

    flags = []
    if approval_gap >= 0.20:
        flags.append("Gap approval rate antar grup tinggi. Perlu ditelusuri apakah perbedaan ini sah, relevan, dan proporsional.")
    if min_di <= 0.80:
        flags.append("Ada grup dengan disparate impact ratio <= 0,80. Ini sinyal awal untuk analisis bias lebih lanjut.")
    if frr_gap >= 0.10:
        flags.append("Gap false rejection rate cukup besar. Perlu cek apakah grup tertentu lebih sering ditolak padahal label aktualnya disetujui.")
    if not flags:
        flags.append("Tidak ada sinyal awal yang menonjol pada data ini, tetapi fairness tetap perlu diuji pada periode dan subgroup lain.")
    return flags


def prepare_lime_encoding(background_data):
    """Encode categorical columns for LIME while preserving original model inputs."""
    encoded_df = background_data.copy()
    category_maps = {}
    categorical_features = []
    categorical_names = {}

    for index, column in enumerate(background_data.columns):
        series = background_data[column]
        is_categorical = (
            is_object_dtype(series.dtype)
            or is_string_dtype(series.dtype)
            or isinstance(series.dtype, pd.CategoricalDtype)
        )

        if is_categorical:
            categories = sorted(series.astype("string").fillna("__MISSING__").unique().tolist())
            mapping = {category: code for code, category in enumerate(categories)}
            encoded_df[column] = (
                series.astype("string")
                .fillna("__MISSING__")
                .map(mapping)
                .fillna(0)
                .astype(float)
            )
            category_maps[column] = categories
            categorical_features.append(index)
            categorical_names[index] = categories
        else:
            encoded_df[column] = pd.to_numeric(series, errors="coerce").fillna(0).astype(float)

    return encoded_df, category_maps, categorical_features, categorical_names


def encode_lime_row(row, category_maps):
    encoded_row = row.copy()
    for column, categories in category_maps.items():
        mapping = {category: code for code, category in enumerate(categories)}
        encoded_row[column] = (
            encoded_row[column]
            .astype("string")
            .fillna("__MISSING__")
            .map(mapping)
            .fillna(0)
            .astype(float)
        )
    return encoded_row


def decode_lime_array(encoded_array, columns, category_maps):
    decoded_df = pd.DataFrame(encoded_array, columns=columns)
    for column, categories in category_maps.items():
        codes = np.rint(decoded_df[column].astype(float)).astype(int)
        decoded_df[column] = codes.apply(
            lambda code: categories[code] if 0 <= code < len(categories) else categories[0]
        )
    return decoded_df


@st.cache_resource
def get_lime_explainer(_background_data, _class_names):
    from lime.lime_tabular import LimeTabularExplainer

    encoded_df, category_maps, categorical_features, categorical_names = prepare_lime_encoding(_background_data)
    explainer = LimeTabularExplainer(
        encoded_df.to_numpy(dtype=float),
        feature_names=list(_background_data.columns),
        class_names=list(_class_names),
        categorical_features=categorical_features,
        categorical_names=categorical_names,
        mode="classification",
        discretize_continuous=True,
        random_state=42,
    )
    return explainer, list(_background_data.columns), category_maps

@st.cache_data
def load_model_and_encoder():
    """Loads the pre-trained model pipeline and label encoder."""
    try:
        with open('credit_approval_model.pkl', 'rb') as f_model:
            model_pipeline = pickle.load(f_model)
        with open('label_encoder.pkl', 'rb') as f_label:
            label_encoder = pickle.load(f_label)
        return model_pipeline, label_encoder
    except FileNotFoundError:
        st.error("File model/encoder tidak ditemukan! Pastikan 'credit_approval_model.pkl' dan 'label_encoder.pkl' berada di direktori yang sama.")
        return None, None

source_df = load_data()
X_background = source_df.drop('Keputusan', axis=1) if source_df is not None else None
model_pipeline, label_encoder = load_model_and_encoder()

# --- 3. SHAP Explainer Setup ---
@st.cache_resource
def get_explainer(_model_pipeline, _background_data):
    """Creates a SHAP KernelExplainer, which is model-agnostic and robust."""
    background_data_summary = shap.sample(_background_data, 100)
    
    # Convert numpy arrays from SHAP back to a DataFrame inside the lambda
    prediction_function = lambda x: _model_pipeline.predict_proba(pd.DataFrame(x, columns=_background_data.columns))
    
    explainer = shap.KernelExplainer(prediction_function, background_data_summary)
    return explainer

if model_pipeline and X_background is not None:
    explainer = get_explainer(model_pipeline, X_background)

# --- 4. Application Title and Description ---
st.title("🤖 Simulasi Audit AI untuk Persetujuan Kredit")
st.markdown("Aplikasi ini mendemonstrasikan bagaimana AI bekerja dalam model persetujuan kredit sederhana.")
st.markdown("---")


# --- 5. User Input Sidebar ---
st.sidebar.header("Masukkan Data Pemohon Pinjaman")
def get_user_input():
    """Collects user input from the sidebar and returns it as a DataFrame."""
    pendapatan = st.sidebar.number_input('Pendapatan Bulanan (Rp)', min_value=1000000, max_value=100000000, value=8000000, step=500000)
    rasio_utang = st.sidebar.slider('Rasio Utang terhadap Pendapatan (%)', min_value=0, max_value=100, value=35)
    skor_slik = st.sidebar.selectbox('Skor SLIK OJK', ['1 - Lancar', '2 - DPK', '3 - Kurang Lancar', '4 - Diragukan', '5 - Macet'])
    pinjaman_aktif = st.sidebar.number_input('Jumlah Pinjaman Aktif', min_value=0, max_value=20, value=2)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Atribut Demografis**")
    jenis_kelamin = st.sidebar.selectbox('Jenis Kelamin', ['Laki-laki', 'Perempuan'])
    suku = st.sidebar.selectbox('Suku', ['Jawa', 'Sunda', 'Batak', 'Bugis', 'Lainnya'])
    jenis_pekerjaan = st.sidebar.selectbox('Jenis Pekerjaan', ['Karyawan Swasta', 'PNS', 'Wiraswasta', 'Pengemudi Online', 'Tidak Bekerja'])
    kode_pos = st.sidebar.selectbox('Kode Pos', ['12190', '50132', '60241', '10110', '14450'], help="Kode pos '14450' berkorelasi dengan suku tertentu.")
    
    input_dict = { 'Pendapatan_Bulanan': pendapatan, 'Rasio_Utang_Pendapatan': rasio_utang, 'Skor_SLIK_OJK': skor_slik, 'Jumlah_Pinjaman_Aktif': pinjaman_aktif, 'Jenis_Kelamin': jenis_kelamin, 'Suku': suku, 'Jenis_Pekerjaan': jenis_pekerjaan, 'Kode_Pos': kode_pos }
    return pd.DataFrame([input_dict], columns=X_background.columns)

input_df = get_user_input()


# --- 6. Prediction and Explanation ---
if 'explainer' in locals() and explainer is not None:
    prediction_encoded = model_pipeline.predict(input_df)[0]
    prediction_decoded = label_encoder.inverse_transform([prediction_encoded])[0]
    prediction_proba = model_pipeline.predict_proba(input_df)[0]
    prob_of_approval = prediction_proba[list(label_encoder.classes_).index('Disetujui')]

    st.subheader("Hasil Prediksi Model")
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="Keputusan", value=prediction_decoded.upper(), delta="✅" if prediction_decoded == 'Disetujui' else "❌", delta_color="normal" if prediction_decoded == 'Disetujui' else "inverse")
    with col2:
        st.metric(label="Probabilitas Persetujuan", value=f"{prob_of_approval:.2%}")

    st.markdown("---")
    st.subheader("Analisis Faktor Keputusan (Model Explainability)")
    st.info("**Cara Membaca Grafik:** Faktor biru mendorong ke arah persetujuan, faktor merah mendorong ke arah penolakan.", icon="💡")
    
    # --- START: Updated SHAP Plotting Logic ---

    # 1. Get the index for the 'Disetujui' (Approved) class
    approval_class_index = list(label_encoder.classes_).index('Disetujui')

    # 2. Generate the SHAP Explanation object using the modern API
    # This call returns a rich object containing values, base values, data, etc.
    shap_explanation = explainer(input_df)

    # 3. Create the plot using the new, simpler syntax
    # We slice the explanation object to get the values for the first sample ([0])
    # and the specific class ('Disetujui').
    fig, ax = plt.subplots(figsize=(10, 6)) # You can adjust figsize if needed
    shap.plots.waterfall(
        shap_explanation[0, :, approval_class_index], # Slicing for the specific instance and class
        max_display=10,
        show=False
    )
    st.pyplot(fig, bbox_inches='tight')
    plt.close(fig) # Close the figure to avoid displaying it twice

    approved_explanation = shap_explanation[0, :, approval_class_index]
    feature_importance_df = pd.DataFrame({
        "Fitur": input_df.columns,
        "Nilai Input": input_df.iloc[0].astype(str).values,
        "Kontribusi SHAP": approved_explanation.values,
    })
    feature_importance_df["Importance Absolut"] = feature_importance_df["Kontribusi SHAP"].abs()
    feature_importance_df["Dampak ke Persetujuan"] = feature_importance_df["Kontribusi SHAP"].apply(
        lambda value: "Menaikkan peluang" if value >= 0 else "Menurunkan peluang"
    )
    feature_importance_df = feature_importance_df.sort_values(
        "Importance Absolut",
        ascending=False
    ).reset_index(drop=True)
    feature_importance_df.insert(0, "Peringkat", feature_importance_df.index + 1)

    st.markdown("**Tabel Feature Importance Lokal**")
    st.caption(
        "Diurutkan berdasarkan pengaruh absolut terhadap prediksi kelas 'Disetujui'. "
        "Nilai SHAP positif menaikkan peluang persetujuan, sedangkan nilai negatif menurunkannya."
    )
    st.dataframe(
        feature_importance_df[[
            "Peringkat",
            "Fitur",
            "Nilai Input",
            "Kontribusi SHAP",
            "Dampak ke Persetujuan",
        ]].style.format({"Kontribusi SHAP": "{:+.4f}"}),
        width="stretch",
        hide_index=True
    )

    # --- END: Updated SHAP Plotting Logic ---

    st.markdown("---")
    st.subheader("LIME Test untuk Prediksi Saat Ini")
    st.caption(
        "LIME membuat variasi lokal di sekitar input saat ini, lalu membangun model sederhana "
        "untuk menjelaskan faktor yang paling memengaruhi prediksi."
    )

    lime_explainer, lime_columns, lime_category_maps = get_lime_explainer(
        X_background,
        tuple(label_encoder.classes_)
    )
    encoded_lime_row = encode_lime_row(input_df, lime_category_maps)

    def lime_predict_proba(encoded_array):
        decoded_df = decode_lime_array(encoded_array, lime_columns, lime_category_maps)
        return model_pipeline.predict_proba(decoded_df)

    lime_explanation = lime_explainer.explain_instance(
        encoded_lime_row.iloc[0].to_numpy(dtype=float),
        lime_predict_proba,
        num_features=8,
        labels=[approval_class_index],
    )
    lime_rows = lime_explanation.as_list(label=approval_class_index)
    lime_df = pd.DataFrame(lime_rows, columns=["Kondisi/Fitur", "Kontribusi LIME"])
    lime_df["Dampak ke Persetujuan"] = lime_df["Kontribusi LIME"].apply(
        lambda value: "Menaikkan peluang" if value >= 0 else "Menurunkan peluang"
    )

    l1, l2 = st.columns([1, 1])
    with l1:
        st.markdown("**Tabel Local Explanation LIME**")
        st.dataframe(
            lime_df.style.format({"Kontribusi LIME": "{:+.4f}"}),
            width="stretch",
            hide_index=True
        )
    with l2:
        st.markdown("**Kontribusi LIME**")
        st.bar_chart(lime_df.set_index("Kondisi/Fitur")["Kontribusi LIME"])

    st.info(
        "Bandingkan hasil LIME dengan SHAP. Jika fitur demografis atau proxy seperti kode pos "
        "muncul kuat di keduanya, itu menjadi sinyal awal untuk fairness review dan penelusuran justifikasi bisnis.",
        icon="💡"
    )

    st.markdown("---")
    st.warning("**TUGAS UNTUK ANDA:** Coba ubah 'Suku', 'Jenis Kelamin', atau 'Kode Pos' dan perhatikan bagaimana grafik penjelasan berubah untuk menemukan bias.", icon="🔬")

    st.markdown("---")
    st.subheader("Fairness Test pada Dataset")
    st.caption(
        "Fairness test membandingkan outcome model antar grup. "
        "Hasil ini adalah sinyal awal untuk diskusi audit, bukan kesimpulan hukum otomatis."
    )

    fairness_col = st.selectbox(
        "Pilih atribut untuk fairness test",
        ["Jenis_Kelamin", "Suku", "Kode_Pos", "Jenis_Pekerjaan"],
        help="Gunakan atribut sensitif atau proxy yang berpotensi memengaruhi outcome model."
    )
    fairness_summary = build_fairness_summary(source_df, model_pipeline, label_encoder, fairness_col)

    highest_approval = fairness_summary.loc[fairness_summary["Approval Rate Model"].idxmax()]
    lowest_approval = fairness_summary.loc[fairness_summary["Approval Rate Model"].idxmin()]
    approval_gap = highest_approval["Approval Rate Model"] - lowest_approval["Approval Rate Model"]
    min_di = fairness_summary["Disparate Impact Ratio"].min()

    f1, f2, f3 = st.columns(3)
    f1.metric("Approval tertinggi", str(highest_approval["Grup"]), f"{highest_approval['Approval Rate Model']:.1%}")
    f2.metric("Approval terendah", str(lowest_approval["Grup"]), f"{lowest_approval['Approval Rate Model']:.1%}")
    f3.metric("Gap approval rate", f"{approval_gap:.1%}", help="Selisih approval rate model antara grup tertinggi dan terendah.")

    st.metric(
        "Minimum disparate impact ratio",
        f"{min_di:.2f}",
        help="Rasio approval rate grup terhadap grup dengan approval rate tertinggi. Nilai rendah menjadi sinyal awal untuk ditelusuri."
    )

    st.markdown("**Ringkasan Fairness per Grup**")
    st.dataframe(
        fairness_summary.style.format({
            "Approval Rate Aktual": "{:.1%}",
            "Approval Rate Model": "{:.1%}",
            "False Approval Rate": "{:.1%}",
            "False Rejection Rate": "{:.1%}",
            "Akurasi": "{:.1%}",
            "Disparate Impact Ratio": "{:.2f}",
        }),
        width="stretch",
        hide_index=True
    )
    st.bar_chart(fairness_summary.set_index("Grup")[["Approval Rate Aktual", "Approval Rate Model"]])

    st.markdown("**Catatan Audit Otomatis**")
    for flag in fairness_flags(fairness_summary):
        st.write(f"- {flag}")

    st.markdown("**Counterfactual Fairness Check untuk Input Saat Ini**")
    st.caption(
        "Aplikasi mengganti satu atribut grup pada input yang sama. "
        "Jika probabilitas berubah tajam hanya karena atribut/proxy grup, auditor perlu menelusuri justifikasi dan dampaknya."
    )
    counterfactual_rows = []
    for group_value in sorted(source_df[fairness_col].dropna().unique()):
        variant_df = input_df.copy()
        variant_df.loc[variant_df.index[0], fairness_col] = group_value
        variant_prediction = label_encoder.inverse_transform(model_pipeline.predict(variant_df))[0]
        variant_proba = model_pipeline.predict_proba(variant_df)[0]
        variant_approval = variant_proba[list(label_encoder.classes_).index('Disetujui')]
        counterfactual_rows.append({
            fairness_col: group_value,
            "Prediksi": variant_prediction,
            "Probabilitas Persetujuan": variant_approval,
            "Selisih dari Input Saat Ini": variant_approval - prob_of_approval,
        })
    st.dataframe(
        pd.DataFrame(counterfactual_rows).style.format({
            "Probabilitas Persetujuan": "{:.2%}",
            "Selisih dari Input Saat Ini": "{:+.2%}",
        }),
        width="stretch",
        hide_index=True
    )

else:
    st.warning("Model atau data tidak dapat dimuat. Aplikasi tidak dapat berjalan.")
