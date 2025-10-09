import streamlit as st
import pandas as pd
import pickle
import shap
import matplotlib.pyplot as plt

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
    """Loads the source dataset to be used as a background for SHAP."""
    try:
        df = pd.read_csv('credit_approval_biased_dataset.csv')
        return df.drop('Keputusan', axis=1)
    except FileNotFoundError:
        return None

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

X_background = load_data()
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

    # --- END: Updated SHAP Plotting Logic ---

    st.markdown("---")
    st.warning("**TUGAS UNTUK ANDA:** Coba ubah 'Suku', 'Jenis Kelamin', atau 'Kode Pos' dan perhatikan bagaimana grafik penjelasan berubah untuk menemukan bias.", icon="🔬")

else:
    st.warning("Model atau data tidak dapat dimuat. Aplikasi tidak dapat berjalan.")