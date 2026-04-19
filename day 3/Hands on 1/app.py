import streamlit as st
import pandas as pd
from etl_pipeline import etl_graph
from io import BytesIO

# Streamlit UI
st.set_page_config(page_title="ETL Pipeline", page_icon="🔄", layout="wide")
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);}
    .stButton>button {background: linear-gradient(45deg, #4CAF50, #45a049); color: white; border-radius: 10px; border: none; padding: 10px 20px; font-size: 16px;}
    .stFileUploader {border: 2px dashed #FFD700; background-color: rgba(255,255,255,0.1); border-radius: 10px;}
    .stDataFrame {border-radius: 10px; background-color: rgba(255,255,255,0.9);}
    h1 {color: #FFD700; text-align: center;}
    h3 {color: #FFFFFF;}
    .stMarkdown {color: #FFFFFF;}
</style>
""", unsafe_allow_html=True)

st.title("🔄 ETL Data Cleaning Pipeline")
st.markdown("**Upload a CSV, clean it with AI-powered transforms, and download the result.**")
st.markdown("---")

with st.sidebar:
    st.header("📋 Instructions")
    st.markdown("- Upload a CSV file.")
    st.markdown("- Preview raw data.")
    st.markdown("- Click 'Process ETL' to clean.")
    st.markdown("- Download cleaned CSV.")
    st.markdown("**Sample Data:** Use `sample_data.csv` for testing.")

uploaded_file = st.file_uploader("📤 Upload CSV", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Raw Data Preview")
    st.dataframe(df.head(), use_container_width=True)
    
    if st.button("🚀 Process ETL"):
        with st.spinner("Processing..."):
            result = etl_graph.invoke({"source": df})
            processed_df = result["data"]
            if "output" in result:
                download_data = result["output"]
            else:
                buffer = BytesIO()
                processed_df.to_csv(buffer, index=False)
                buffer.seek(0)
                download_data = buffer
        
        st.subheader("✅ Cleaned Data Preview")
        st.dataframe(processed_df.head(), use_container_width=True)
        
        st.download_button(
            label="📥 Download Cleaned CSV",
            data=download_data,
            file_name="cleaned_data.csv",
            mime="text/csv"
        )
