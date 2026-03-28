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
            st.subheader("Generated Content")
            st.code(result, language=None)
            st.download_button(
                label="Download as .txt",
                data = result,
                file_name = f"{content_type.lower().replace(" ","_")}.txt",
                mime = "text/plain",
                use_container_width = True
            )

              


if st.session_state.history:
    st.divider()
    st.subheader("Generation History")

    for i, item in enumerate(reversed(st.session_state.history)):
        with st.expander(f"{item['type']} - {item['topic']}"):
            st.code(item['result'], language=None)
            st.download_button(
                label = "Download as .txt",
                data = item['result'],
                file_name = f"{item['type'].lower().replace(' ','_')}.txt",
                mime= "text/plain",
                use_container_width= True,
                key=f"download_{i}" 
            )
