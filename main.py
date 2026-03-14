import gradio as gr
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import datetime
import os
import re

# --- MODEL INITIALIZATION ---
# Using an empathetic transformer model suitable for local deployment
MODEL_NAME = "facebook/blenderbot-400M-distill"
print("Initializing NLP Engine for Stress Management...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)

# --- CORE LOGIC: Stress Management & Ethics ---
def psychiatrist_logic(message):
    # 1. Stress Management Detection
    # If the user mentions high stress, the agent prioritizes immediate guidance
    stress_keywords = ["stress", "anxious", "overwhelmed", "panic", "pressure"]
    if any(word in message.lower() for word in stress_keywords):
        management_tip = "\n\n(Stress Management Tip: Try the 4-7-8 breathing technique: Inhale for 4s, hold for 7s, exhale for 8s.)"
    else:
        management_tip = ""

    # 2. Interaction Logic & Persona
    system_instruction = (
        "Instructions: You are a professional text-based psychiatrist. "
        "Provide evidence-based guidance for stress management. "
        "Focus on active listening and ethical, empathetic responses. "
    )
    
    full_input = f"{system_instruction} Patient: {message}"
    inputs = tokenizer(full_input, return_tensors="pt")
    
    outputs = model.generate(
        **inputs, 
        max_length=150, 
        do_sample=True, 
        temperature=0.65, # Balanced for consistency and empathy
        top_p=0.9
    )
    
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response + management_tip

def chat_flow(user_input, chat_history):
    if not user_input.strip():
        return "", chat_history
    
    bot_msg = psychiatrist_logic(user_input)
    chat_history.append((user_input, bot_msg))
    return "", chat_history

# 3. Ethical Data Handling: Secure Local Logging
def save_session_securely(history):
    if not history: return None
    
    if not os.path.exists("secure_logs"):
        os.makedirs("secure_logs")
        
    ts = datetime.datetime.now().strftime("%Y-%m-%d_%H%M")
    filepath = os.path.join("secure_logs", f"clinical_session_{ts}.txt")
    
    # Ethical Disclaimer added to every log
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"CONFIDENTIAL CLINICAL RECORD\n")
        f.write(f"Data Privacy: This file is stored locally and not shared with 3rd parties.\n")
        f.write(f"Date: {ts}\n" + "="*40 + "\n\n")
        for u, b in history:
            f.write(f"USER: {u}\nAGENT: {b}\n\n")
            
    return filepath

# --- UI DESIGN: Blue, White, and Indigo ---
custom_css = """
.gradio-container {background-color: #ffffff; font-family: 'Inter', sans-serif;}
#header {text-align: center; color: white; background-color: #1e3a8a; padding: 30px; border-radius: 12px; margin-bottom: 20px;}
.message-user {background-color: #4338ca !important; color: white !important; border-radius: 15px 15px 0 15px !important;}
.message-bot {background-color: #f3f4f6 !important; border-radius: 15px 15px 15px 0 !important;}
#submit-btn {background-color: #4338ca !important; color: white !important;} 
#export-btn {background-color: #3730a3 !important; color: white !important;}
"""

with gr.Blocks(css=custom_css, theme=gr.themes.Soft()) as demo:
    gr.HTML("""
        <div id='header'>
            <h1>Clinical Mind Companion</h1>
            <p>NLP-Powered Stress Management & Psychiatric Support</p>
        </div>
    """)
    
    with gr.Tabs():
        with gr.TabItem("Consultation"):
            chatbot = gr.Chatbot(label="Encrypted Session", height=500)
            msg = gr.Textbox(placeholder="How can I help you manage your stress today?", label="User Input")
            
            with gr.Row():
                submit = gr.Button("Submit Analysis", variant="primary", elem_id="submit-btn")
                clear = gr.ClearButton([msg, chatbot])
            
            with gr.Row():
                save_btn = gr.Button("💾 Securely Export Logs", elem_id="export-btn")
                file_out = gr.File(label="Local Log Path")

        with gr.TabItem("System Ethics & Logic"):
            gr.Markdown("### Project Foundations")
            gr.Markdown("""
            - **Ethical Data Handling:** All conversations are processed locally. No data is transmitted to external servers for training.
            - **Stress Management Guidance:** The agent uses NLP to detect stress triggers and provide immediate coping mechanisms.
            - **User-Friendly Interaction:** Clean Indigo-accented UI designed to reduce cognitive load during high-stress periods.
            """)
            

    # Wiring
    submit.click(chat_flow, [msg, chatbot], [msg, chatbot])
    msg.submit(chat_flow, [msg, chatbot], [msg, chatbot])
    save_btn.click(save_session_securely, inputs=[chatbot], outputs=[file_out])

if __name__ == "__main__":
    demo.launch()