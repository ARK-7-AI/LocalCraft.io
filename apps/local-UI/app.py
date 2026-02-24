import re
import streamlit as st
import requests
import json

# Configuration
RENDER_URL = "https://localcraft-io.onrender.com/get-next"
OLLAMA_BASE_URL = "http://localhost:11434"


def reset_app():
    # --- Reset Main Areas ---
    st.session_state["jd_input_key"] = ""
    st.session_state["prompt_input_key"] = ""
    st.session_state["ai_output"] = ""
    st.session_state["jd_text"] = ""

    # --- Reset Sidebar Sliders ---
    st.session_state["word_count_key"] = 300
    st.session_state["temp_key"] = 0.7

    st.toast("App Reset! Ready for a new request.")


st.set_page_config(page_title="LocalCraft AI", layout="wide")

# --- UI Header ---
st.title("🤖 LocalCraft: Agnostic LLM Bridge")
st.caption("Connected to Render Cloud & Local Ollama Daemon")

# --- Sidebar: Model Discovery ---
with st.sidebar:
    st.header("Local Model Settings")
    try:
        tags_res = requests.get(f"{OLLAMA_BASE_URL}/api/tags")
        if tags_res.status_code == 200:
            model_list = [m['name'] for m in tags_res.json().get('models', [])]

            selected_model = st.selectbox(
                "Select Installed Model",
                model_list
            )

            st.success(f"Connected to {len(model_list)} models")

            st.divider()

            # --- Generation Settings ---
            st.header("Generation Settings")

            target_words = st.slider(
                "Target Word Count",
                100, 800,
                300, 50,
                key="word_count_key",
                help="Sets the maximum length. 300 is ideal for cover letters."
            )

            token_limit = int(target_words / 0.75) + 50

            temp = st.slider(
                "Creativity (Temperature)",
                0.0, 1.0,
                0.7, 0.1,
                key="temp_key",
                help="Higher is more creative; 0.7 is perfect for professional writing."
            )

            st.divider()

            st.button("🔄 Reset All Fields", on_click=reset_app)

        else:
            st.error("Ollama returned an error.")
            selected_model = None

    except:
        st.error("Ollama Daemon not found. Is it running?")
        selected_model = None
        st.info("Tip: Start the Ollama app and refresh this page.")


# --- Main Interface ---
col1, col2 = st.columns(2)


def clean_jd(raw_text):
    if not raw_text:
        return ""

    text = re.sub(r'\[\d+(?:,\s*\d+)*\]', '', raw_text)

    boilerplate_keywords = [
        "Recruitment Fraud Alert",
        "Equal Opportunity Employer",
    ]

    for key in boilerplate_keywords:
        if key in text:
            text = text.split(key)[0]

    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'^About the job\s+', '', text, flags=re.IGNORECASE)

    return text.strip()


# --- Column 1: JD ---
with col1:
    st.subheader("Step 1: Fetch Context")

    if st.button("📥 Pull JD from Cloud"):
        with st.spinner("Fetching JD ..."):
            try:
                res = requests.get(RENDER_URL)
                data = res.json()

                if data.get("jd"):
                    cleaned = clean_jd(data["jd"])
                    st.session_state["jd_input_key"] = cleaned
                else:
                    st.info("Queue is empty. Please extract new JD from plugin.")

            except Exception as e:
                st.error(f"Cloud Connection Failed: {e}")

    jd_input = st.text_area(
        "Job Description",
        height=300,
        key="jd_input_key"
    )


# --- Column 2: Prompt ---
with col2:
    st.subheader("Step 2: Generation")

    user_prompt = st.text_area(
        "Custom Instructions",
        placeholder="e.g. Highlight my Master's in AI and research...",
        height=100,
        key="prompt_input_key"
    )

    if st.button("🚀 Generate Results"):
        if not selected_model:
            st.error("Please select a model in the sidebar.")
        elif not jd_input:
            st.warning("No JD context found.")
        else:
            with st.spinner(f"Processing with {selected_model}..."):

                payload = {
                    "model": selected_model,
                    "prompt": f"Context:\n{jd_input}\n\nTask: {user_prompt}",
                    "stream": False,
                    "options": {
                        "temperature": temp,
                        "num_predict": token_limit,
                        "num_ctx": 4096
                    }
                }

                try:
                    response = requests.post(
                        f"{OLLAMA_BASE_URL}/api/generate",
                        json=payload
                    )

                    data = response.json()
                    st.session_state["ai_output"] = data.get("response", "")

                except Exception as e:
                    st.error(f"LLM Error: {e}")


# --- Result Area ---
if st.session_state.get("ai_output"):
    st.divider()
    st.subheader("Final Output")
    st.text_area(
        "Edit Output",
        value=st.session_state["ai_output"],
        height=300,
        key="ai_output"
    )
