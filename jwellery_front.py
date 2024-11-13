import streamlit as st
import requests
from PIL import Image
import pandas as pd
import os
# FastAPI URL
GENERATE_CAPTION_URL = "http://65.0.131.103/generate_caption"

# Create the Streamlit interface
st.set_page_config(page_title="Generate jwellery descriptions", layout="wide")
st.title("Generate jwellery descriptions")
# Allow user to upload multiple images
uploaded_files = st.file_uploader("Upload images", type=['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff'], accept_multiple_files=True)

# Initialize a session state to keep track of uploaded images
if 'images' not in st.session_state:
    st.session_state.images = []

# Add newly uploaded images to the session state
if uploaded_files:
    for uploaded_file in uploaded_files:
        # Avoid adding duplicates
        if uploaded_file not in st.session_state.images:
            st.session_state.images.append(uploaded_file)
headings = [
    "Elegance",
    "Charm",
    "Luxury",
    "Modernity",
    "Timelessness",
    "Delicacy",
    "Boldness",
    "Romance",
    "Earthiness",
    "Artistry"
    ]
jewelry_styles = {
    "Elegance": "Jewelry that embodies sophistication, adding a refined touch suitable for formal settings.",
    "Charm": "Pieces that convey a sense of warmth and appeal, making them endearing and delightful.",
    "Luxury": "Reflects an aura of exclusivity and high quality, perfect for those seeking something special.",
    "Modernity": "Captures contemporary styles, appealing to those who appreciate current trends and innovation.",
    "Timelessness": "Designs that maintain appeal across eras, suitable for those who value enduring style.",
    "Delicacy": "Jewelry with a gentle and subtle quality, often associated with a soft, graceful appearance.",
    "Boldness": "Makes a statement with a strong presence, ideal for those who prefer impactful designs.",
    "Romance": "Pieces that evoke a sense of love and sentimentality, often carrying a romantic or heartfelt appeal.",
    "Earthiness": "Connects to natural elements or grounded aesthetics, appealing to those with a down-to-earth style.",
    "Artistry": "Showcases creativity and craftsmanship, appealing to individuals who appreciate unique designs."
}

selections = [] 
# Show uploaded images with the option to remove them
if st.session_state.images:
    cols = st.columns(5)  # Create a column for each image
    for i, img in enumerate(st.session_state.images):
        with cols[i%5]:
            st.image(img, caption=img.name, width=150)
            selected_option = st.selectbox(
                f"Choose option for Image {img.name}",
                headings,
                index=headings.index("Elegance"),
                key=f"select_{img.name}"
            )
            selections.append(jewelry_styles[selected_option]) 
            

# Button to generate captions
if st.button("Generate Captions"):
    

    if st.session_state.images:
        # Prepare images for the request (limited to 100 images)
        files = [('files', (img.name, img, img.type)) for img in st.session_state.images]
        # Send POST request to FastAPI to generate captions
        response = requests.post(GENERATE_CAPTION_URL, files=files,json={"types":selections})

        if response.status_code == 200:
            output_file = "output.csv"
            with open(output_file, "wb") as f:
                f.write(response.content)

            # Store response and DataFrame in session state
            st.session_state.response = response
            st.session_state.df = pd.read_csv(output_file)
            st.table(st.session_state.df)

            # Provide a download button for the user to download the CSV
            with open(output_file, "rb") as f:
                st.download_button("Download CSV", f, file_name="gemini_output.csv", mime="text/csv")
            
            # Optionally clean up the file after download
            os.remove(output_file)
        else:
            st.error("Error generating captions.")
    else:
        st.error("Please upload images and enter a User ID.")



