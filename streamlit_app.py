import streamlit as st
from utils.generator import generate_content

st.set_page_config(
    page_title="AI Content Studio",
    page_icon="✍️",
    layout="centered"
)


st.markdown("""
<style>
    .main { padding-top: 2rem; }
    .stButton > button {
        background-color: #6C63FF;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1rem;
        font-weight: 600;
        width: 100%;
        transition: background-color 0.2s;
    }
    .stButton > button:hover {
        background-color: #5a52d5;
        color: white;
    }
    .stDownloadButton > button {
        background-color: transparent;
        color: #6C63FF;
        border: 1.5px solid #6C63FF;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    .stDownloadButton > button:hover {
        background-color: #6C63FF;
        color: white;
    }
    .stSelectbox > div > div {
        border-radius: 8px;
    }
    .stTextInput > div > div > input {
        border-radius: 8px;
    }
    .content-box {
        background-color: #f8f9ff;
        border: 1px solid #e0deff;
        border-radius: 12px;
        padding: 1.5rem;
        font-size: 0.95rem;
        line-height: 1.8;
        color: #2d2d2d;
        white-space: pre-wrap;
        margin-bottom: 1rem;
    }
    .history-meta {
        font-size: 0.78rem;
        color: #888;
        margin-bottom: 0.3rem;
    }
    .badge {
        display: inline-block;
        background-color: #ede9ff;
        color: #6C63FF;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def copy_button(text, key):
    escaped = text.replace("`", "\\`").replace("\n", "\\n")
    st.markdown(f"""
    <button class="copy-btn" onclick="navigator.clipboard.writeText(`{escaped}`).then(() => {{
        this.innerText = 'Copied!';
        setTimeout(() => this.innerText = 'Copy to clipboard', 2000);
    }})">Copy to clipboard</button>
    """, unsafe_allow_html=True)



st.markdown("## ✍️ AI Content Studio")
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

if "history" not in st.session_state:
    st.session_state.history=[]

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic first")
    else:
        with st.spinner("Generating Content...."):
            result = generate_content(content_type, topic)

            st.session_state.history.append(
                {
                    "type" : content_type,
                    "topic" : topic,
                    "result" : result
                }
            )

            st.divider()
            st.markdown("#### Generated Content")
            st.markdown(f'<div class="badge">{content_type}</div>', unsafe_allow_html=True)
            
            
            with st.container():
                st.markdown('<div class="content-area">', unsafe_allow_html=True)
                st.markdown(result)
                st.markdown('</div>', unsafe_allow_html=True)

            copy_button(result, key="main")    
            st.download_button(
                label="Download as .txt",
                data = result,
                file_name = f"{content_type.lower().replace(" ","_")}.txt",
                mime = "text/plain",
                use_container_width = True
            )

              


if st.session_state.history:
    st.divider()
    st.markdown("#### Generation History")

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{item['type']} - {item['topic']}"):
            st.markdown(f'<div class="badge">{item["type"]}</div>', unsafe_allow_html=True)
            st.markdown('<div class="content-area">', unsafe_allow_html=True)
            st.markdown(item["result"])
            st.markdown('</div>', unsafe_allow_html=True)
            copy_button(item["result"], key=f"copy_{i}")

            st.download_button(
                label = "Download as .txt",
                data = item['result'],
                file_name = f"{item['type'].lower().replace(' ','_')}.txt",
                mime= "text/plain",
                use_container_width= True,
                key=f"download_{i}" 
            )
