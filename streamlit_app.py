import streamlit as st
from utils.generator import generate_content

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✍️",
    layout="centered"
)

st.title("✍️ AI Content Studio")
st.caption("Generate professional content using AI in seconds")
st.divider()

topic= st.text_input(
    "Enter the topic",
    placeholder="eg. The Future of AI"
)


content_type = st.selectbox(
    "Choose content type",
    ["Blog Post","LinkedIn Caption","Cold Email"]
)

generate_button = st.button("Generate", type="primary", use_container_width=True)

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic first")
    else:
        with st.spinner("Generating Content...."):
            result = generate_content(content_type, topic)

            st.divider()
            st.subheader("Generated Content")
            st.write(result)
