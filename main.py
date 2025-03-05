import streamlit as st
import time
import base64
from scrape import scrape_web, split_dom, clean_body_content, extract_body
from parse import parse_with_ollama

# Set Streamlit page layout & title
st.set_page_config(page_title="Web Scraper", layout="wide")

# Convert local image (17263.jpg) to Base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

# Set background image (Ensure 17263.jpg is in the same directory)
bg_image_base64 = get_base64_of_image("backgroundimg.jpg")

# Custom CSS for a blurred background & blue color theme
st.markdown(f"""
    <style>
        /* Remove Navbar */
        header {{
            visibility: hidden;
        }}

        /* Background Image with Blur */
        .stApp {{
            background: url("data:image/jpg;base64,{bg_image_base64}") no-repeat center center fixed;
            background-size: cover;
        }}

        /* Dark overlay to enhance readability */
        .stApp::before {{
            content: "";
            position: absolute;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: rgba(0, 0, 50, 0.6);  /* Dark blue overlay */
            backdrop-filter: blur(5px);
            z-index: -1;
        }}

        /* Centered title */
        .title-text {{
            font-size: 40px;
            font-weight: bold;
            text-align: center;
            color: #FFD700;
            margin-bottom: 20px;
        }}

        /* Centering container */
        .main-container {{
            max-width: 600px;
            margin: auto;
            padding: 30px;
        }}

        /* Input fields */
        .stTextInput > div > div > input, 
        .stTextArea > div > textarea {{
            border-radius: 8px;
            background-color: rgba(255, 255, 255, 0);
            color: #ffffff;
            border: 1px solid #00A6FB; /* Light blue border */
            transition: 0.3s ease-in-out;
        }}

        .stTextInput > div > div > input:focus, 
        .stTextArea > div > textarea:focus {{
            border-color: #0084d6; /* Darker blue */
            background-color: rgba(255, 255, 255, 0.1);
        }}

        /* Buttons */
        .stButton > button {{
            background: linear-gradient(to right, #0072B5, #005F87);
            color: white;
            font-weight: bold;
            border-radius: 12px;
            padding: 12px;
            width: 100%;
            border: none;
            transition: all 0.3s ease-in-out;
            box-shadow: 0px 4px 10px rgba(0, 114, 181, 0.3);
        }}

        .stButton > button:hover {{
            background: linear-gradient(to right, #005F87, #003F5C);
            box-shadow: 0px 6px 14px rgba(0, 95, 135, 0.2);
        }}

        /* Card-style container */
        .container {{
            background: rgba(255, 255, 255, 0.1);
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(8px);
            margin-bottom: 20px;
        }}
    </style>
""", unsafe_allow_html=True)

# Page Title
st.markdown('<h2 class="title-text">Advanced Web Scraper</h2>', unsafe_allow_html=True)

# Main content container
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.subheader("Enter Website URL")
url = st.text_input("", placeholder="https://example.com")

if st.button("Scrape Site"):
    if url:
        with st.spinner("Scraping the webpage..."):
            time.sleep(2)  # Simulate loading
            result = scrape_web(url)
            body_content = extract_body(result)
            cleaned_content = clean_body_content(body_content)

            st.session_state.dom_content = cleaned_content
            st.success("Webpage scraped successfully.")

# Show extracted content
if "dom_content" in st.session_state:
    with st.expander("View Extracted Content", expanded=False):
        st.text_area("", st.session_state.dom_content, height=300)

# Divider
st.markdown("---")

# Data Extraction Section
if "dom_content" in st.session_state:
    st.subheader("Extract Data")

    parse_description = st.text_area("Describe what data you need", placeholder="Extract product details, article headlines, etc.")

    if st.button("Process Data"):
        if parse_description:
            with st.spinner("Analyzing content..."):
                time.sleep(2)  # Simulate loading

                dom_chunks = split_dom(st.session_state.dom_content)
                result = parse_with_ollama(dom_chunks, parse_description)

                st.subheader("Extracted Data")
                st.write(result)
        else:
            st.warning("Please enter a description of the data you want to extract.")

# Close main container
st.markdown('</div>', unsafe_allow_html=True)
