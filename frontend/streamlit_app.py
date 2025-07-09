import os

import httpx
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RULES_DIR = os.path.join(BASE_DIR, "app", "validation_rules")

API_URL = os.getenv("BACKEND_URL", "http://localhost:8080")
DEFAULT_API_KEY = os.getenv("API_KEY", "supersecreta")

st.set_page_config(page_title="🧪 Data Validator", layout="centered")
st.title("📊 Data Quality Validator")

st.markdown(
    "Upload a CSV file to run automated data validation and profiling.\n"
    "- A downloadable cleaned dataset\n"
    "- A validation report\n"
    "- A profiling report"
)

with st.sidebar:
    st.title("⚙️ Settings")
    api_key = st.text_input("API Key", value=DEFAULT_API_KEY, type="password")

    try:
        if os.path.isdir(RULES_DIR):
            a = [f for f in os.listdir(RULES_DIR) if f.endswith(".json")]
        else:
            a = []
            st.warning("⚠️ Validation rules directory not found.")
    except FileNotFoundError:
        a = []
        st.warning("⚠️ No validation rules found.")

    rules_file = st.selectbox("Validation Rules", a)

uploaded_file = st.file_uploader("📎 Upload CSV File", type=["csv"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    preview = uploaded_file.getvalue().decode("utf-8").splitlines()[:10]
    st.dataframe(preview)

    if st.button("🚀 Run Validation"):
        with st.spinner("Validating... please wait."):
            try:
                endpoint = f"{API_URL}/validate/?rules_file={rules_file}"
                headers = {"x-api-key": api_key}
                files = {"file": (uploaded_file.name, uploaded_file)}

                response = httpx.post(endpoint, headers=headers, files=files)

                if response.status_code == 200:
                    result = response.json()
                    hash_id = result["hash"]
                    st.success("✅ Validation completed successfully!")

                    csv_url = f"{API_URL}/datasets/file/{hash_id}"
                    csv_response = httpx.get(csv_url, headers=headers)
                    if csv_response.status_code == 200:
                        st.download_button(
                            "⬇️ Download Cleaned CSV",
                            csv_response.content,
                            file_name=uploaded_file.name,
                        )
                    else:
                        st.warning("⚠️ Could not download cleaned CSV.")

                    report_url = f"{API_URL}/reports/{hash_id}"
                    report_response = httpx.get(report_url, headers=headers)
                    if report_response.status_code == 200:
                        with st.expander("📄 Validation Report"):
                            st.components.v1.html(
                                report_response.text,
                                height=600,
                                scrolling=True,
                            )

                    profile_url = f"{API_URL}/profiles/{hash_id}"
                    profile_response = httpx.get(profile_url, headers=headers)
                    if profile_response.status_code == 200:
                        with st.expander("📊 Profiling Report"):
                            st.components.v1.html(
                                profile_response.text,
                                height=600,
                                scrolling=True,
                            )
                else:
                    st.error(
                        f"❌ Validation failed: {response.status_code} - "
                        f"{response.text}"
                    )
            except Exception as e:
                st.error(f"❌ Unexpected error: {str(e)}")
else:
    st.info("📥 Upload a CSV file to begin.")
