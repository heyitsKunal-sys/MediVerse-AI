from dotenv import load_dotenv
load_dotenv()

import os
import gradio as gr

from brain_of_AI import encode_image, analyze_image_with_query
from voice_of_patient import transcribe_with_groq
from voice_of_the_doctor import text_to_speech


# ======================================================
# SYSTEM PROMPT
# ======================================================

system_prompt = """
You have to act as a professional doctor.
What's in this image? Do you find anything wrong with it medically?
If you make a differential, suggest some remedies.
Do not add numbers or special characters.
Answer like a real doctor.
Keep the answer concise.
"""


# ======================================================
# CUSTOM CSS
# The whole app is wrapped in a single #app-shell div (see UI section
# below). #app-shell owns the border / radius / shadow / max-height,
# NOT .gradio-container -- Gradio manipulates .gradio-container's own
# sizing internally, which is what caused the border/margin bugs
# before. This way our frame is independent of that and stays intact
# on every screen size.
# ======================================================

css = """
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=IBM+Plex+Mono:wght@500;600&display=swap');

:root{
    --bg-1:#eef6f5;
    --bg-2:#e1efec;
    --surface:#ffffff;
    --ink:#0b2b2b;
    --ink-soft:#52706e;
    --teal:#0e7c7b;
    --teal-deep:#0a5c5b;
    --mint:#cdeee6;
    --coral:#ff5a5f;
    --coral-deep:#e14549;
    --line:#dbeae6;
}

*{
    box-sizing:border-box;
}

html, body{
    margin:0 !important;
    padding:0 !important;
    height:100%;
    overflow:hidden;
}

body{
    background:
        radial-gradient(circle at 15% 0%, #f4faf9 0%, transparent 45%),
        linear-gradient(160deg, var(--bg-1) 0%, var(--bg-2) 55%, #d8ece7 100%);
    font-family:'Inter', sans-serif;
}

/* ---------------- OUTER SHELL (Gradio's own wrapper) ---------------- */
/* Neutralised: no border/padding/max-width here anymore, it just
   centers our real frame (#app-shell) in the viewport. */

.gradio-container{
    box-sizing:border-box !important;
    width:100% !important;
    height:100vh !important;
    max-width:none !important;
    margin:0 !important;
    padding:16px !important;
    background:transparent !important;
    display:flex !important;
    align-items:flex-start !important;
    justify-content:center !important;
    overflow:hidden !important;
}

/* ---------------- THE ACTUAL FRAME ---------------- */

#app-shell{
    width:100% !important;
    max-width:1180px !important;
    max-height:calc(100vh - 32px) !important;
    overflow-y:auto !important;
    overflow-x:hidden !important;
    box-sizing:border-box !important;
    border:2px solid var(--teal) !important;
    border-radius:24px !important;
    background:linear-gradient(180deg, #f6fbfa 0%, #eef6f5 100%) !important;
    box-shadow:0 20px 50px rgba(10,60,58,0.14) !important;
    padding:22px 26px 16px !important;
    color:var(--ink);
    font-family:'Inter', sans-serif;
}

#app-shell::-webkit-scrollbar{ width:8px; }
#app-shell::-webkit-scrollbar-thumb{ background:var(--mint); border-radius:8px; }

@media (max-width: 768px){
    .gradio-container{ padding:8px !important; }
    #app-shell{
        max-height:calc(100vh - 16px) !important;
        padding:14px 12px 10px !important;
        border-radius:18px !important;
    }
}

/* ---------------- HERO ---------------- */

.hero{
    position:relative;
    text-align:center;
    padding:14px 10px 16px;
}

.hero-badges{
    display:flex;
    justify-content:center;
    gap:10px;
    margin-bottom:14px;
    flex-wrap:wrap;
}

.hero-badge{
    font-family:'IBM Plex Mono', monospace;
    font-size:11px;
    letter-spacing:0.08em;
    text-transform:uppercase;
    color:var(--teal-deep);
    background:var(--surface);
    border:1px solid var(--line);
    padding:6px 14px;
    border-radius:999px;
    box-shadow:0 2px 8px rgba(10,92,91,0.08);
}

.main-title{
    font-family:'Space Grotesk', sans-serif;
    font-size:32px;
    font-weight:700;
    color:var(--ink);
    margin:0 0 6px;
    letter-spacing:-0.01em;
}

.main-title span{
    color:var(--teal);
}

.subtitle{
    font-family:'Inter', sans-serif;
    font-size:14px;
    color:var(--ink-soft);
    margin-bottom:16px;
}

.ecg-wrap{
    width:100%;
    max-width:460px;
    margin:0 auto;
    opacity:0.9;
}

.ecg-line{
    stroke:var(--coral);
    stroke-width:2.4;
    fill:none;
    stroke-linecap:round;
    stroke-linejoin:round;
    stroke-dasharray:900;
    stroke-dashoffset:900;
    animation:draw-ecg 3.4s ease-in-out infinite;
}

@keyframes draw-ecg{
    0%{stroke-dashoffset:900;}
    45%{stroke-dashoffset:0;}
    85%{stroke-dashoffset:0; opacity:1;}
    100%{stroke-dashoffset:-900; opacity:0.4;}
}

.disclaimer{
    font-family:'IBM Plex Mono', monospace;
    font-size:10.5px;
    color:var(--ink-soft);
    text-align:center;
    letter-spacing:0.02em;
    padding:10px 10px 4px;
    max-width:640px;
    margin:0 auto;
}

/* ---------------- SECTION EYEBROWS ---------------- */

.eyebrow{
    font-family:'IBM Plex Mono', monospace;
    font-size:12px;
    font-weight:600;
    letter-spacing:0.12em;
    text-transform:uppercase;
    color:var(--teal-deep);
    display:flex;
    align-items:center;
    gap:8px;
    margin:0 0 8px;
    padding-left:2px;
}

.eyebrow::before{
    content:"";
    width:8px;
    height:8px;
    border-radius:50%;
    background:var(--coral);
    box-shadow:0 0 0 4px rgba(255,90,95,0.15);
    flex-shrink:0;
}

/* ---------------- PANELS / CARDS ---------------- */

.panel{
    background:var(--surface);
    border-radius:16px;
    border:1px solid var(--line);
    box-shadow:0 10px 24px rgba(10,60,58,0.07);
    padding:16px 18px 10px !important;
    margin-bottom:14px;
}

.gradio-container .block{
    border-radius:14px !important;
    border-color:var(--line) !important;
}

/* form component labels look like chart field labels */
label span, .gr-label, label{
    font-family:'IBM Plex Mono', monospace !important;
    font-size:11.5px !important;
    letter-spacing:0.04em;
    color:var(--teal-deep) !important;
    text-transform:uppercase;
}

textarea, input[type="text"]{
    border-radius:12px !important;
    border-color:var(--line) !important;
    font-family:'Inter', sans-serif !important;
    color:var(--ink) !important;
}

textarea:focus, input[type="text"]:focus{
    border-color:var(--teal) !important;
    box-shadow:0 0 0 3px rgba(14,124,123,0.14) !important;
}

/* upload / dropzone areas -- capped height so they don't dominate
   the viewport on smaller screens */
.upload-box, [data-testid="image"], [data-testid="audio"]{
    border-radius:14px !important;
    min-height:120px !important;
}

.upload-box{
    border:1.5px dashed var(--teal) !important;
    background:linear-gradient(180deg, #f6fbfa, #eef8f6) !important;
    transition:0.25s ease;
}

.upload-box:hover{
    border-color:var(--coral) !important;
    background:#fbf3f2 !important;
}

/* ---------------- BUTTONS ---------------- */

button{
    border-radius:12px !important;
    font-family:'Space Grotesk', sans-serif !important;
    font-weight:600 !important;
    letter-spacing:0.01em;
    transition:transform 0.2s ease, box-shadow 0.2s ease !important;
    border:none !important;
}

button:hover{
    transform:translateY(-2px);
}

.primary, button.primary, #submit-btn{
    background:linear-gradient(135deg, var(--coral), var(--coral-deep)) !important;
    color:#fff !important;
    box-shadow:0 10px 24px rgba(255,90,95,0.35) !important;
}

.primary:hover{
    box-shadow:0 14px 30px rgba(255,90,95,0.45) !important;
}

.secondary, button.secondary, #clear-btn{
    background:var(--surface) !important;
    color:var(--teal-deep) !important;
    border:1.5px solid var(--line) !important;
    box-shadow:none !important;
}

.secondary:hover{
    border-color:var(--teal) !important;
    background:var(--mint) !important;
}

footer{ display:flex !important; }

@media (max-width: 768px){
    .main-title{ font-size:24px; }
    .subtitle{ font-size:12.5px; }
    .hero-badge{ font-size:10px; padding:5px 10px; }
}
"""


# ======================================================
# MAIN FUNCTION
# ======================================================

def process_inputs(audio_filepath, image_filepath):

    # Speech To Text
    if audio_filepath is None:
        speech_to_text_output = "No audio provided."

    else:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )

    # Image Analysis
    if image_filepath is not None:

        encoded_img = encode_image(image_filepath)

        doctor_response = analyze_image_with_query(
            query=system_prompt + "\n" + speech_to_text_output,
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            encoded_image=encoded_img
        )

    else:
        doctor_response = (
            "No image was uploaded. Please upload a medical image."
        )

    # Text To Speech
    audio_path = text_to_speech(
        text=doctor_response,
        output_file="final.mp3"
    )

    return (
        speech_to_text_output,
        doctor_response,
        audio_path
    )


# ======================================================
# UI
# ======================================================

with gr.Blocks(
    css=css,
    theme=gr.themes.Soft(
        primary_hue="teal",
        secondary_hue="red",
        font=[gr.themes.GoogleFont("Inter"), "sans-serif"],
    ),
    title="MediVerse AI Doctor"
) as iface:

    # Everything lives inside this single wrapping column -- THIS is
    # what gets the border / frame / max-height, not .gradio-container.
    with gr.Column(elem_id="app-shell"):

        # Hero Section

        gr.HTML("""
        <div class="hero">
            <div class="hero-badges">
                <span class="hero-badge">👁 Vision</span>
                <span class="hero-badge">🎙 Voice</span>
                <span class="hero-badge">🧠 AI Analysis</span>
            </div>
            <div class="main-title">MediVerse <span>AI Doctor</span></div>
            <div class="subtitle">Describe what you feel. Show what you see. Get a read on it.</div>
            <div class="ecg-wrap">
                <svg viewBox="0 0 600 60" xmlns="http://www.w3.org/2000/svg">
                    <path class="ecg-line" d="M0,30 L130,30 L155,8 L180,52 L205,15 L230,30 L360,30 L385,10 L410,50 L435,18 L460,30 L600,30" />
                </svg>
            </div>
        </div>
        """)

        with gr.Row():

            # LEFT SIDE — INTAKE

            with gr.Column(scale=1, elem_classes="panel"):

                gr.HTML('<div class="eyebrow">Intake — 01</div>')

                audio_input = gr.Audio(
                    sources=["microphone"],
                    type="filepath",
                    label="Describe Your Symptoms"
                )

                image_input = gr.Image(
                    type="filepath",
                    label="Upload Medical Image"
                )

            # RIGHT SIDE — READOUT

            with gr.Column(scale=1, elem_classes="panel"):

                gr.HTML('<div class="eyebrow">Readout — 02</div>')

                speech_output = gr.Textbox(
                    label="Speech Recognition",
                    lines=2
                )

                doctor_output = gr.Textbox(
                    label="Doctor Analysis",
                    lines=5
                )

                audio_output = gr.Audio(
                    type="filepath",
                    label="AI Doctor Voice"
                )

        # BUTTONS

        with gr.Row():

            clear_btn = gr.ClearButton(
                components=[
                    audio_input,
                    image_input,
                    speech_output,
                    doctor_output,
                    audio_output
                ],
                value="Clear",
                elem_id="clear-btn",
                elem_classes="secondary"
            )

            submit_btn = gr.Button(
                "Analyze Medical Condition",
                variant="primary",
                elem_id="submit-btn",
                elem_classes="primary"
            )

        gr.HTML("""
        <div class="disclaimer">
            MediVerse is an AI assistant, not a licensed physician.
            For emergencies or serious symptoms, contact a real doctor.
        </div>
        """)

    # FUNCTION CONNECTION

    submit_btn.click(
        fn=process_inputs,
        inputs=[
            audio_input,
            image_input
        ],
        outputs=[
            speech_output,
            doctor_output,
            audio_output
        ]
    )

# ======================================================
# LAUNCH
# ======================================================
if __name__ == "__main__":
    iface.launch(
        debug=True,
        share=False
    )
