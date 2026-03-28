import streamlit as st
from utils.generator import generate_content
import json
import streamlit.components.v1 as components

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
    .stButton > button:hover { background-color: #5a52d5; color: white; }
    .stDownloadButton > button {
        background-color: transparent;
        color: #6C63FF;
        border: 1.5px solid #6C63FF;
        border-radius: 8px;
        font-weight: 500;
        width: 100%;
    }
    .stDownloadButton > button:hover { background-color: #6C63FF; color: white; }
    .stSelectbox > div > div { border-radius: 8px; }
    .stTextInput > div > div > input { border-radius: 8px; }
    .badge {
        display: inline-block;
        background-color: #ede9ff;
        color: #6C63FF;
        border-radius: 20px;
        padding: 2px 12px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


def copy_button(text):
    safe_text = json.dumps(text)
    components.html(f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;background:transparent;">
            <button id="copybtn"
                style="
                    background-color: transparent;
                    border: 1.5px solid #6C63FF;
                    color: #6C63FF;
                    border-radius: 8px;
                    padding: 6px 16px;
                    font-size: 14px;
                    font-weight: 500;
                    cursor: pointer;
                    font-family: sans-serif;
                ">
                Copy to clipboard
            </button>
            <script>
                var textToCopy = {safe_text};
                document.getElementById("copybtn").addEventListener("click", function() {{
                    navigator.clipboard.writeText(textToCopy).then(function() {{
                        document.getElementById("copybtn").innerText = "Copied!";
                        setTimeout(function() {{
                            document.getElementById("copybtn").innerText = "Copy to clipboard";
                        }}, 2000);
                    }});
                }});
            </script>
        </body>
        </html>
    """, height=45)


def display_result(content_type, topic, result, download_key):
    st.markdown(f'<div class="badge">{content_type}</div>', unsafe_allow_html=True)
    st.markdown(result)
    st.divider()
    copy_button(result)
    st.download_button(
        label="Download as .txt",
        data=result,
        file_name=f"{content_type.lower().replace(' ', '_')}.txt",
        mime="text/plain",
        use_container_width=True,
        key=download_key
    )


st.markdown("## ✍️ AI Content Studio")
st.caption("Generate professional content using AI in seconds")
st.divider()

topic = st.text_input(
    "Enter the topic",
    placeholder="e.g. The Future of AI"
)

content_type = st.selectbox(
    "Choose content type",
    ["Blog Post", "LinkedIn Caption", "Cold Email"]
)

generate_button = st.button("Generate", type="primary", use_container_width=True)

if "history" not in st.session_state:
    st.session_state.history = []

if st.session_state.history and not isinstance(st.session_state.history[0], dict):
    st.session_state.history = []

if generate_button:
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Generating content..."):
            result = generate_content(content_type, topic)

        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state.history.append({
                "type": content_type,
                "topic": topic,
                "result": result
            })

if st.session_state.history:
    latest = st.session_state.history[-1]
    st.divider()
    st.markdown("#### Generated Content")
    display_result(
        latest["type"],
        latest["topic"],
        latest["result"],
        download_key=f"download_main_{len(st.session_state.history)}"
    )

if len(st.session_state.history) > 1:
    st.divider()
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("#### Generation History")
    with col2:
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = st.session_state.history[-1:]
            st.rerun()

    for i, item in enumerate(reversed(st.session_state.history[:-1])):
        with st.expander(f"{item['type']} — {item['topic']}"):
            display_result(
                item["type"],
                item["topic"],
                item["result"],
                download_key=f"download_history_{i}"
            )