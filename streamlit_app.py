import streamlit as st
from utils.generator import generate_content, improve_content
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
    .stTextArea > div > div > textarea { border-radius: 8px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.4rem 1rem;
        font-weight: 500;
    }
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
    .word-count {
        font-size: 0.78rem;
        color: #888;
        margin-top: 0.3rem;
        margin-bottom: 0.5rem;
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
    word_count = len(result.split())
    st.markdown(f'<div class="word-count">{word_count} words</div>',
                unsafe_allow_html=True)
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

# --- Session state init ---
for key in ["history", "last_topic", "last_content_type"]:
    if key not in st.session_state:
        st.session_state[key] = [] if key =="history" else ""

if st.session_state.history and not isinstance(st.session_state.history[0], dict):
    st.session_state.history = []

# --- Main tabs ---
tab_generate, tab_improve = st.tabs(["Generate Content", "Improve My Draft"])

# =====================
# TAB 1 — GENERATE
# =====================
with tab_generate:
    topic = st.text_input(
        "Enter the topic",
        placeholder="e.g. The Future of AI in Hiring"
    )

    content_type = st.selectbox(
        "Choose content type",
        ["Blog Post", "LinkedIn Caption", "Cold Email"]
    )

    col1, col2 = st.columns([3, 1])

    with col1:
        generate_btn = st.button(
            "Generate",
            type="primary",
            use_container_width=True,
            key="btn_generate"
        )


    with col2:
        regenerate_btn = st.button(
            "Regenerate",
            use_container_width=True,
            key="btn_regenerate"
        
        )

    # Generate single
    if generate_btn:
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            st.session_state.variations = []
            with st.spinner("Generating content..."):
                result = generate_content(content_type, topic)

            if result.startswith("Error:"):
                st.error(result)
            else:
                st.session_state.last_topic = topic
                st.session_state.last_content_type = content_type
                st.session_state.history.append({
                    "type": content_type,
                    "topic": topic,
                    "result": result
                })

    # Regenerate
    if regenerate_btn and st.session_state.last_topic:
        st.session_state.variations = []
        with st.spinner("Regenerating..."):
            result = generate_content(
                st.session_state.last_content_type,
                st.session_state.last_topic
            )

        if result.startswith("Error:"):
            st.error(result)
        else:
            st.session_state.history.append({
                "type": st.session_state.last_content_type,
                "topic": st.session_state.last_topic,
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

    # History
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

# =====================
# TAB 2 — IMPROVE
# =====================
with tab_improve:
    st.markdown("Paste your existing draft and get an improved version instantly.")

    improve_content_type = st.selectbox(
        "Content type of your draft",
        ["Blog Post", "LinkedIn Caption", "Cold Email"],
        key="improve_type"
    )

    draft = st.text_area(
        "Paste your draft here",
        placeholder="Paste your existing blog post, caption, or email...",
        height=200
    )

    improve_btn = st.button(
        "Improve My Draft",
        type="primary",
        use_container_width=True,
        key="btn_improve"
    )

    if improve_btn:
        if not draft.strip():
            st.warning("Please paste your draft first.")
        elif len(draft.split()) < 10:
            st.warning("Draft is too short — please paste at least a few sentences.")
        else:
            with st.spinner("Improving your draft..."):
                improved = improve_content(improve_content_type, draft)

            if improved.startswith("Error:"):
                st.error(improved)
            else:
                st.divider()
                st.markdown("#### Improved Version")
                display_result(
                    improve_content_type,
                    "Improved draft",
                    improved,
                    download_key="download_improved"
                )