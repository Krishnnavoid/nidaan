# 📐 Nidaan (निदान) — AI Diagnostic Math Tutor

> **Hackathon Prototype** | Class 8 Linear Equations
> Diagnosing **WHY** a student is wrong before teaching them.

---

## 🌟 Overview
Nidaan (निदान) is an intelligent AI tutoring assistant designed for Indian school students (Class 8). Instead of simply giving the right answer when a student makes a mistake, Nidaan uses a **buggy-rule misconception engine** and **Sarvam AI**'s Indic reasoning models to:
1. Detect conceptual misconceptions vs. careless slips.
2. Probe student understanding with targeted mathematical variants.
3. Deliver concise, empathetic micro-explanations in Hindi & English.

---

## 🚀 Live Demo & Deployment
- **Deployment Platform:** [Streamlit Community Cloud](https://share.streamlit.io/)
- **Repository:** [https://github.com/Krishnnavoid/nidaan](https://github.com/Krishnnavoid/nidaan)
- **Main file path:** `app.py`

### Deploying to Streamlit Cloud:
1. Fork or push this repository to GitHub: `https://github.com/Krishnnavoid/nidaan`.
2. Go to [share.streamlit.io](https://share.streamlit.io) and click **"New app"**.
3. Select repository `Krishnnavoid/nidaan`, branch `main`, and main file `app.py`.
4. In **Advanced settings** -> **Secrets**, add your Sarvam AI API Key:
   ```toml
   SARVAM_API_KEY = "your_actual_sarvam_api_key_here"
   ```
5. Click **Deploy!**

---

## 🛠️ Tech Stack
- **Frontend / UI:** Python 3.10+, Streamlit
- **Math Verification:** SymPy
- **AI & Indic Language Engine:** [Sarvam AI APIs](https://docs.sarvam.ai) (`sarvam-105b` model)
- **Configuration & Secrets:** `python-dotenv`

---

## 💻 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Krishnnavoid/nidaan.git
   cd nidaan
   ```

2. **Create a virtual environment & install dependencies:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux / macOS:
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure your API Key:**
   Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   Add your Sarvam AI API Key in `.env`:
   ```env
   SARVAM_API_KEY=your_actual_api_key_here
   ```
   *(Note: `.gitignore` protects your `.env` and `sarvam.evm` from ever being committed)*

4. **Run the Streamlit app:**
   ```bash
   streamlit run app.py
   ```
   Visit `http://localhost:8501` in your browser.

5. **Run tests:**
   ```bash
   python -m unittest tests/test_sarvam.py
   ```

---

## 🗺️ Roadmap
- [x] **Step 1:** Setup & Sarvam AI Client integration
- [ ] **Step 2:** Misconception Engine (SymPy Buggy Rules)
- [ ] **Step 3:** Read-Back Confirmation UI
- [ ] **Step 4:** Probe & Verdict Engine
- [ ] **Step 5:** Targeted Micro-Teaching via Sarvam Chat
- [ ] **Step 6:** Explain-Back Reasoning Checker
- [ ] **Step 7:** Student Profile Persistence (`profile.json`)
- [ ] **Step 8:** Voice Integration (Sarvam STT & TTS)
