import streamlit as st
import requests
import json
from PIL import Image
import io
import base64
import os

# Set page config
st.set_page_config(
    page_title="UXO Detection System",
    page_icon="⚠️",
    layout="wide"
)

# Custom CSS for government-style theme
st.markdown("""
    <style>
    .main {
        background-color: #E6F3FF;
    }
    .stApp {
        background-color: #E6F3FF;
    }
    .stButton>button {
        background-color: #003366;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #004080;
    }
    .warning {
        color: #CC0000;
        font-weight: bold;
        background-color: #FFE6E6;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #CC0000;
    }
    .info {
        color: #003366;
        background-color: #E6F3FF;
        padding: 15px;
        border-radius: 5px;
        border-left: 5px solid #003366;
    }
    .title {
        color: #003366;
        font-size: 2.5em;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    .description {
        color: #333333;
        font-size: 1.1em;
        line-height: 1.6;
        margin-bottom: 30px;
        text-align: justify;
        background-color: white;
        padding: 20px;
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .section-title {
        color: #003366;
        font-size: 1.8em;
        font-weight: bold;
        margin-top: 30px;
        margin-bottom: 20px;
        border-bottom: 2px solid #003366;
        padding-bottom: 10px;
    }
    .stFileUploader>div>div>div>div {
        background-color: white;
    }
    .stImage>div>div>img {
        border-radius: 5px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# API endpoints from environment variables
CLASSIFIER_API = os.getenv("CLASSIFIER_API", "http://classifier:5000/classify")
DETECTOR_API = os.getenv("DETECTOR_API", "http://detector:8000/detect")

# Title and Description
st.markdown('<h1 class="title">Underwater Unexploded Ordnances (UXOs) Identification and Detection Tool</h1>', unsafe_allow_html=True)

st.markdown("""
    <div class="description">
    This tool serves as an indicator for the presence of UXOs, which denote all kind of ordnances that have not exploded after launching, particularly underwater. 
    If you are near a body of water and suspect of the presence of a UXO, please maintain your distance, contact the Lebanese Mine Action Center (LMAC) at +961 5 956 143, 
    and take a snapshot with your phone at a distance to detect whether the suspected object is likely to be a UXO. Aside from image data, this tool can also classify sonar data, 
    a feature designed for professionals in the field with access to the needed tools such as ARIS 3000.
    </div>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["UXO Classification", "UXO Detection"])

if page == "UXO Classification":
    st.markdown('<h2 class="section-title">UXO Classification</h2>', unsafe_allow_html=True)
    st.write("Upload sonar data image to classify if it contains UXO")
    
    uploaded_file = st.file_uploader("Choose a sonar data image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        # Convert to RGB if image has alpha channel
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGB')
        st.image(image, caption="Uploaded Sonar Image", use_column_width=True)
        
        if st.button("Classify"):
            try:
                # Save the uploaded file temporarily
                temp_path = "temp_image.jpg"
                image.save(temp_path, format='JPEG')
                
                # Send file to classification API
                with open(temp_path, 'rb') as f:
                    files = {"file": f}
                    response = requests.post(CLASSIFIER_API, files=files)
                
                # Clean up temp file
                os.remove(temp_path)
                
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        if result["prediction"] == 1:  # UXO detected
                            st.markdown('<p class="warning">WARNING! You are within a close distance of a UXO, please evacuate and contact the Lebanese Mine Action Center (LMAC) at +961 5 956 143 immediately!</p>', unsafe_allow_html=True)
                        else:  # No UXO detected
                            st.markdown('<p class="info">The uploaded sonar is not likely to be a UXO, but it is recommended that you maintain a distance and report the location to the Lebanese Mine Action Center (LMAC) at +961 5 956 143</p>', unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {result['message']}")
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.error(f"Error details: {response.text}")
                    
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")

elif page == "UXO Detection":
    st.markdown('<h2 class="section-title">UXO Detection</h2>', unsafe_allow_html=True)
    st.write("Upload an image to detect UXO with bounding boxes")
    
    uploaded_image = st.file_uploader("Choose an image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded_image is not None:
        # Display the uploaded image
        image = Image.open(uploaded_image)
        # Convert to RGB if image has alpha channel
        if image.mode in ('RGBA', 'LA') or (image.mode == 'P' and 'transparency' in image.info):
            image = image.convert('RGB')
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        if st.button("Detect"):
            try:
                # Save the uploaded file temporarily
                temp_path = "temp_image.jpg"
                image.save(temp_path, format='JPEG')
                
                # Send image to detection API
                with open(temp_path, 'rb') as f:
                    files = {"file": f}
                    response = requests.post(DETECTOR_API, files=files)
                
                # Clean up temp file
                os.remove(temp_path)
                
                if response.status_code == 200:
                    result = response.json()
                    if result["status"] == "success":
                        # Display annotated image
                        img_data = base64.b64decode(result["annotated_image"])
                        annotated_img = Image.open(io.BytesIO(img_data))
                        st.image(annotated_img, caption="Detected UXO", use_column_width=True)
                        
                        # Display warning message based on detections
                        if result["detections"]:  # If there are any detections
                            st.markdown('<p class="warning">WARNING! You are within a close distance of a UXO, please evacuate and contact the Lebanese Mine Action Center (LMAC) at +961 5 956 143 immediately!</p>', unsafe_allow_html=True)
                        else:
                            st.markdown('<p class="info">The uploaded image is not likely to contain a UXO, but it is recommended that you maintain a distance and report the location to the Lebanese Mine Action Center (LMAC) at +961 5 956 143</p>', unsafe_allow_html=True)
                    else:
                        st.error(f"Error: {result['message']}")
                else:
                    st.error(f"API Error: {response.status_code}")
                    st.error(f"Error details: {response.text}")
                    
            except Exception as e:
                st.error(f"Error connecting to API: {str(e)}")
                st.error("Please make sure the detection API is running and accessible.") 