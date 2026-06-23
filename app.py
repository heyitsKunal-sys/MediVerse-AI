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
# ======================================================

css = """
body{
    background:url('/file=assets/background.jpg');
    background-size:cover;
    background-position:center;
    background-attachment:fixed;
}

.gradio-container{
    background:rgba(255,255,255,0.10);
    backdrop-filter:blur(10px);
}

.hero{
    text-align:center;
    padding:20px;
}

.logo{
    width:120px;
    margin-bottom:15px;
    animation:float 3s ease-in-out infinite;
}

@keyframes float{
    0%{transform:translateY(0px);}
    50%{transform:translateY(-10px);}
    100%{transform:translateY(0px);}
}

.main-title{
    font-size:48px;
    font-weight:bold;
    color:#0f172a;
    margin-bottom:10px;
}

.subtitle{
    font-size:18px;
    color:#334155;
}

.panel{
    background:white;
    border-radius:20px;
    padding:20px;
    box-shadow:0px 10px 30px rgba(0,0,0,.15);
}

button{
    border-radius:15px !important;
    transition:0.3s ease;
}

button:hover{
    transform:translateY(-3px);
}

textarea{
    border-radius:15px !important;
}

footer{
    margin-top:20px;
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
    theme=gr.themes.Soft()
) as iface:

    # Hero Section

    gr.HTML("""
    <div class="hero">

        <img src="" class="logo">

        <div class="main-title">
            🩺 MediVerse AI Doctor
        </div>

        <div class="subtitle">
            AI Powered Medical Assistant with Vision + Voice
        </div>

    </div>
    """)

    with gr.Row():

        # LEFT SIDE

        with gr.Column(scale=1):

            audio_input = gr.Audio(
                sources=["microphone"],
                type="filepath",
                label="🎤 Describe Your Symptoms"
            )

            image_input = gr.Image(
                type="filepath",
                label="🩻 Upload Medical Image"
            )

        # RIGHT SIDE

        with gr.Column(scale=1):

            speech_output = gr.Textbox(
                label="📝 Speech Recognition",
                lines=3
            )

            doctor_output = gr.Textbox(
                label="🩺 Doctor Analysis",
                lines=8
            )

            audio_output = gr.Audio(
                type="filepath",
                label="🔊 AI Doctor Voice"
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
            value="🗑 Clear"
        )

        submit_btn = gr.Button(
            "🚀 Analyze Medical Condition",
            variant="primary"
        )

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
