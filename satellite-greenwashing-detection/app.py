import streamlit as st
import requests
from vegetation_detection import detect_vegetation
from graph_generator import create_graph

st.title("Satellite Greenwashing Detection System")

# Option 1: Upload image
uploaded_file = st.file_uploader("Upload Satellite Image")

# Option 2: Enter image URL
image_url = st.text_input("Or paste image URL")

image_path = "input.jpg"

# If user uploads image
if uploaded_file:
    
    with open(image_path,"wb") as f:
        f.write(uploaded_file.getbuffer())

    st.image(uploaded_file)

# If user enters URL
elif image_url:

    response = requests.get(image_url)

    with open(image_path,"wb") as f:
        f.write(response.content)

    st.image(image_url)

else:
    st.info("Upload an image or paste an image URL.")

# Run analysis if image exists
try:
    veg, nonveg, heatmap, status = detect_vegetation(image_path)

    if status == "Valid":

        create_graph(veg, nonveg)

        st.subheader("Vegetation Heatmap")
        st.image(heatmap)

        st.write("Vegetation Area:", round(veg,2), "%")
        st.write("Non Vegetation Area:", round(nonveg,2), "%")

        st.image("coverage_graph.png")

        if veg < 30:
            st.error("⚠ Possible Greenwashing Detected")
        else:
            st.success("Vegetation Coverage Looks Good")

except:
    pass