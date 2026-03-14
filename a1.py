import streamlit as st
import pyttsx3
import tempfile
import os
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# -------------------------------
# 1. Processor: Connect to Ollama
# -------------------------------
def process_text_with_ollama(raw_text):
    """
    Sends text to local Ollama instance (Llama3/Mistral) and returns structured notes, flowchart, and audio script.
    """
    llm = OllamaLLM(model="llama3")

    template = """
    You are a study assistant. Convert the following text into three parts:

    1. # Detailed Notes (Markdown format)
    2. Mermaid.js flowchart code starting with 'graph TD'
    3. Audio Script (simplified, easy-to-read text for speech)

    Text: {raw_text}

    Return in this format:

    # Detailed Notes
    <markdown notes>

    graph TD
    <mermaid flowchart>

    Audio Script:
    <audio-friendly text>
    """

    prompt = PromptTemplate(template=template, input_variables=["raw_text"])
    chain = LLMChain(llm=llm, prompt=prompt)

    response = chain.run(raw_text)

    # Split response into sections
    notes, flowchart, audio_script = "", "", ""
    if "# Detailed Notes" in response:
        parts = response.split("graph TD")
        notes = parts[0].replace("# Detailed Notes", "").strip()
        if len(parts) > 1:
            flow_parts = parts[1].split("Audio Script:")
            flowchart = "graph TD" + flow_parts[0].strip()
            if len(flow_parts) > 1:
                audio_script = flow_parts[1].strip()

    return notes, flowchart, audio_script


# -------------------------------
# 2. Audio Engine: pyttsx3
# -------------------------------
def generate_audio(audio_text):
    """
    Converts text to speech using pyttsx3 and returns path to temporary audio file.
    """
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.setProperty("volume", 1.0)

    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
    engine.save_to_file(audio_text, tmp_file.name)
    engine.runAndWait()
    return tmp_file.name


# -------------------------------
# 3. Streamlit Frontend
# -------------------------------
st.set_page_config(page_title="Learning Pack Generator", layout="wide")

st.title("📚 Local Learning Pack Generator")
st.write("Convert raw text into notes, flowcharts, and audio — all offline!")

raw_text = st.text_area("Enter your content:", height=200)

if st.button("Generate Learning Pack"):
    if raw_text.strip():
        with st.spinner("Processing with Ollama..."):
            notes, flowchart, audio_script = process_text_with_ollama(raw_text)

        # Tabs for Read, Watch, Listen
        tab1, tab2, tab3 = st.tabs(["📖 Read", "🎥 Watch", "🔊 Listen"])

        with tab1:
            st.markdown("### Detailed Notes")
            st.markdown(notes)

        with tab2:
            st.markdown("### Flowchart")
            # Inject Mermaid with fade-in animation
            mermaid_html = f"""
            <div class="mermaid">
            {flowchart}
            </div>
            <script>
            mermaid.initialize({{ startOnLoad: true }});
            document.addEventListener("DOMContentLoaded", function() {{
                const svg = document.querySelector("svg");
                if (svg) {{
                    const elements = svg.querySelectorAll("*");
                    elements.forEach((el, i) => {{
                        el.style.opacity = 0;
                        setTimeout(() => {{
                            el.style.transition = "opacity 1s";
                            el.style.opacity = 1;
                        }}, i * 200);
                    }});
                }}
            }});
            </script>
            """
            st.components.v1.html(mermaid_html, height=500, scrolling=True)

        with tab3:
            st.markdown("### Audio Playback")
            if audio_script:
                audio_file = generate_audio(audio_script)
                with open(audio_file, "rb") as f:
                    audio_bytes = f.read()
                st.audio(audio_bytes, format="audio/mp3")
                os.remove(audio_file)
            else:
                st.warning("No audio script generated.")
    else:
        st.error("Please enter some text before generating.")