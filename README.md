🩺 MediVerse-AI

AI-Powered Medical Chatbot with Vision and Voice Assistance

MediVerse-AI is an advanced multimodal healthcare assistant that leverages the power of Generative AI, Computer Vision, Speech Recognition, and Natural Voice Synthesis to provide intelligent preliminary medical guidance.

The system can analyze medical images, understand patient symptoms through voice input, generate contextual healthcare responses using a Large Language Model (LLM), and respond back with realistic AI-generated speech.

---

🚀 Features

👁️ Medical Image Analysis

- Upload medical images for AI-powered analysis.
- Supports skin conditions, visible injuries, infections, and other image-based observations.
- Uses Meta Llama 4 Scout multimodal capabilities.

🎙️ Voice-Based Symptom Input

- Users can describe symptoms naturally using their voice.
- Audio is recorded and processed automatically.

📝 Speech-to-Text Conversion

- Powered by Whisper Large V3 via Groq Cloud.
- Converts spoken symptoms into accurate text transcripts.

🧠 AI Medical Reasoning

- Uses Meta Llama 4 Scout 17B 16E Instruct.
- Analyzes image data and symptom descriptions simultaneously.
- Generates contextual healthcare recommendations.

🔊 Natural Voice Responses

- Powered by ElevenLabs Text-to-Speech.
- Converts AI-generated responses into realistic human speech.

🌐 Interactive Web Interface

- Built using Gradio.
- Supports image uploads, voice recording, and real-time responses.

---

🏗️ System Architecture

User Input (Image + Voice)
│
▼
Gradio Interface
│
▼
Voice Recording
(PyAudio + PortAudio)
│
▼
Audio Processing
(FFmpeg)
│
▼
Whisper Large V3
(Speech-to-Text)
│
▼
Meta Llama 4 Scout
(Medical Reasoning)
│
▼
AI Medical Response
│
▼
ElevenLabs TTS
│
▼
Voice Response
│
▼
User

---

🛠️ Tech Stack

Programming Language

- Python

AI & Machine Learning

- Groq Cloud API
- Meta Llama 4 Scout 17B 16E Instruct
- Whisper Large V3

Voice Processing

- PyAudio
- PortAudio
- FFmpeg

Text-to-Speech

- ElevenLabs API

User Interface

- Gradio

Environment Management

- Python Dotenv

---

📂 Project Structure

MediVerse-AI/
│
├── app.py
├── gradio_app.py
├── brain_of_AI.py
├── voice_of_patient.py
├── voice_of_the_doctor.py
├── requirements.txt
├── .env
├── .gitignore
├── assets/
│   └── logo.png
│
└── README.md

📖 Module Description

brain_of_AI.py

Responsible for:

- Image Encoding
- Prompt Engineering
- Groq API Communication
- Medical Response Generation

Functions:

encode_image()
analyze_image_with_query()

---

voice_of_patient.py

Responsible for:

- Audio Recording
- Speech-to-Text Conversion
- Audio Processing

Functions:

record_audio()
transcribe_with_groq()

---

voice_of_the_doctor.py

Responsible for:

- Text-to-Speech Generation
- Audio Playback

Functions:

text_to_speech()

---

gradio_app.py

Responsible for:

- User Interface
- Image Upload
- Audio Input
- Response Display

---

⚙️ Installation

Clone Repository

git clone https://github.com/yourusername/MediVerse-AI.git
cd MediVerse-AI

Create Virtual Environment

python -m venv venv

Activate Environment

Windows

venv\Scripts\activate

Linux / Mac

source venv/bin/activate

---

Install Dependencies

pip install -r requirements.txt

---

🔑 Environment Variables

Create a ".env" file in the project root.

GROQ_API_KEY=your_groq_api_key
ELEVENLABS_API_KEY=your_elevenlabs_api_key

---

▶️ Run the Application

python gradio_app.py

The application will start locally and can be accessed through:

http://127.0.0.1:7860

---

💡 How It Works

Step 1

User uploads a medical image.

Step 2

User describes symptoms using voice.

Step 3

PyAudio records the audio.

Step 4

FFmpeg processes the audio.

Step 5

Whisper Large V3 converts speech into text.

Step 6

Image and symptoms are sent to Meta Llama 4 Scout.

Step 7

The model generates a medical response.

Step 8

ElevenLabs converts the response into speech.

Step 9

The final response is displayed and spoken to the user.

---

🎯 Use Cases

- Preliminary Symptom Assessment
- Medical Image Interpretation
- Healthcare Assistance
- AI-Powered Telemedicine Support
- Voice-Based Health Consultation
- Accessibility Support for Elderly Users

---

⚠️ Disclaimer

MediVerse-AI is designed for educational and research purposes only.

The system does not provide professional medical diagnosis and should not replace consultation with qualified healthcare professionals.

Always seek advice from certified medical practitioners for diagnosis and treatment.

---

🔮 Future Scope

- Retrieval-Augmented Generation (RAG)
- Medical Knowledge Base Integration
- Electronic Health Records (EHR)
- Multilingual Support (Hindi, Punjabi, etc.)
- Mobile Application Development
- Medical Report Analysis
- Real-Time Video Consultation
- Wearable Device Integration

---



---

"Empowering Healthcare Through Multimodal Artificial Intelligence."