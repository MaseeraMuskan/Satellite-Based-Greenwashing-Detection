import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO
import plotly.express as px

from predict import predict

# PAGE SETTINGS
st.set_page_config(
    page_title="Satellite Greenwashing Detection",
    layout="wide"
)

# CUSTOM STYLE
st.markdown("""
<style>

.metric-box {
    padding:20px;
    border-radius:12px;
    background:linear-gradient(135deg,#3CB371,#2E8B57);
    color:white;
    text-align:center;
    font-size:20px;
}

</style>
""", unsafe_allow_html=True)

st.title("🌍 Satellite Based Greenwashing Detection System")

st.write("AI-based vegetation and environmental monitoring using satellite imagery")

# SIDEBAR INPUT
st.sidebar.header("Input Image")

url = st.sidebar.text_input("Satellite Image URL")

uploaded_file = st.sidebar.file_uploader(
    "Upload Satellite Image",
    type=["jpg","jpeg","png"]
)

image = None

# LOAD URL IMAGE
if url.strip() != "":
    try:
        if url.startswith("http"):
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=10)

            if "image" in response.headers.get("Content-Type",""):
                image = Image.open(BytesIO(response.content)).convert("RGB").resize((224,224))
            else:
                st.sidebar.warning("The URL does not contain an image.")

    except Exception as e:
        st.sidebar.warning("Could not load image from URL.")

# LOAD UPLOADED IMAGE
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB").resize((224,224))

# PROCESS IMAGE
if image is not None:

    img = np.array(image)/255.0

    ndvi, urban, pollution, score, ndvi_map = predict(img)

    # IMAGE + METRICS
    col1, col2 = st.columns([1,2])

    with col1:
        st.subheader("Satellite Image")
        st.image(image)

    with col2:

        m1, m2, m3, m4 = st.columns(4)

        m1.metric("Greenwashing Score", f"{score:.2f}%")
        m2.metric("NDVI Index", f"{ndvi:.2f}")
        m3.metric("Urban Index", f"{urban:.2f}")
        m4.metric("Pollution Index", f"{pollution:.2f}")

    st.divider()

    # HEATMAP + GRAPH
    col3, col4 = st.columns(2)

    with col3:

        st.subheader("Vegetation Heatmap")

        fig, ax = plt.subplots()

        heatmap = ax.imshow(ndvi_map, cmap="YlGn")

        plt.colorbar(heatmap)

        st.pyplot(fig)

    with col4:

        st.subheader("Vegetation Pixel Distribution")

        fig2 = px.histogram(
            ndvi_map.flatten(),
            nbins=40
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # VEGETATION COVERAGE BAR
    vegetation_pixels = np.sum(ndvi_map > 0.3)
    total_pixels = ndvi_map.size

    vegetation_percent = (vegetation_pixels/total_pixels)*100

    st.subheader("Vegetation Coverage")

    st.progress(int(vegetation_percent))

    st.write(f"Vegetation Coverage: **{vegetation_percent:.2f}%**")

    st.divider()

    # RISK STATUS
    st.subheader("Environmental Risk Status")

    if score > 60:

        st.error("⚠ HIGH GREENWASHING RISK")

    elif score > 30:

        st.warning("⚠ MODERATE GREENWASHING RISK")

    else:

        st.success("✔ ECO-FRIENDLY ENVIRONMENT")