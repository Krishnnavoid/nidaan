"""
Nidaan (निदान) - AI Diagnostic Math Tutor
Prototype for Hackathon - Class 8 Linear Equations
"""

import time
import streamlit as st
from sarvam_client import get_api_key, test_sarvam_chat, DEFAULT_CHAT_MODEL

# -----------------------------------------------------------------------------
# Page Configuration
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Nidaan (निदान) AI Tutor",
    page_icon="📐",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# Custom Styling (Vanilla CSS)
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Global styles */
    .stApp {
        background: linear-gradient(180deg, #fbfbfd 0%, #f4f6fa 100%);
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Header Card */
    .nidaan-header {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        color: white;
        padding: 1.8rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 25px -5px rgba(15, 23, 42, 0.15);
        margin-bottom: 2rem;
        border-left: 6px solid #f97316;
    }
    
    .nidaan-title {
        font-size: 2.1rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 0.6rem;
    }
    
    .nidaan-tagline {
        color: #94a3b8;
        font-size: 0.98rem;
        margin-top: 0.4rem;
        margin-bottom: 0;
    }
    
    /* Status Badge */
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-top: 0.8rem;
    }
    
    .badge-success {
        background-color: rgba(34, 197, 94, 0.15);
        color: #15803d;
        border: 1px solid rgba(34, 197, 94, 0.3);
    }
    
    .badge-danger {
        background-color: rgba(239, 68, 68, 0.15);
        color: #b91c1c;
        border: 1px solid rgba(239, 68, 68, 0.3);
    }
    
    /* Card Container */
    .custom-card {
        background-color: #ffffff;
        border-radius: 14px;
        padding: 1.5rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03);
        margin-bottom: 1.5rem;
    }
    
    /* Response Box */
    .response-box {
        background-color: #f8fafc;
        border-radius: 10px;
        border-left: 4px solid #3b82f6;
        padding: 1.2rem;
        font-size: 1.05rem;
        line-height: 1.6;
        color: #1e293b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="nidaan-header">
        <div class="nidaan-title">
            <span>📐 Nidaan (निदान)</span>
        </div>
        <p class="nidaan-tagline">
            Diagnostic AI Math Tutor for Class 8: Diagnosing <em>WHY</em> students make errors before teaching.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# API Key Verification
# -----------------------------------------------------------------------------
api_key = get_api_key()

# Sidebar Setup
with st.sidebar:
    st.header("⚙️ Configuration")
    if api_key:
        st.markdown(
            '<div class="status-badge badge-success">● SARVAM_API_KEY Configured</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<div class="status-badge badge-danger">● SARVAM_API_KEY Missing</div>',
            unsafe_allow_html=True,
        )
    
    st.divider()
    st.subheader("📌 Project Roadmap")
    st.markdown(
        """
        - **Step 1:** Setup & Sarvam AI Client *(Active)*
        - **Step 2:** Misconception Engine (SymPy)
        - **Step 3:** Read-Back Confirmation
        - **Step 4:** Probe & Verdict UI
        - **Step 5:** Targeted Micro-Teaching
        - **Step 6:** Explain-Back Reasoning Check
        - **Step 7:** Student Profile Persistence
        - **Step 8:** Voice (STT & TTS)
        """
    )

if not api_key:
    st.error(
        """
        ### ⚠️ Sarvam API Key Missing
        No `SARVAM_API_KEY` was found in your `.env` or `sarvam.evm` file.
        
        **How to fix:**
        1. Open `sarvam.evm` (or create `.env`) in the project directory.
        2. Add your key like this:
           ```env
           SARVAM_API_KEY=your_actual_sarvam_key_here
           ```
        3. Save the file and refresh this page.
        """
    )
    st.info("💡 Note: Your `.gitignore` is already configured to keep your key secure and private.")
    st.stop()

# -----------------------------------------------------------------------------
# Step 1: Sarvam AI Connection Test Interface
# -----------------------------------------------------------------------------
st.markdown("### 🧪 Step 1: Sarvam AI Integration Test")
st.write(
    "Verify the live connection with Sarvam AI's chat completion API "
    f"(`{DEFAULT_CHAT_MODEL}`) in Hindi / English."
)

with st.container():
    test_prompt = st.text_input(
        "Test Prompt (Hindi or English):",
        value="नमस्ते! मैं कक्षा 8 का छात्र हूँ। क्या आप मुझे रैखिक समीकरण सिखा सकते हैं?",
        help="Custom prompt to send to Sarvam AI chat endpoint",
    )
    
    col1, col2 = st.columns([1, 3])
    with col1:
        run_test = st.button("🚀 Test Connection", type="primary", use_container_width=True)
        
    if run_test:
        with st.spinner("Connecting to Sarvam AI (`sarvam-105b`)..."):
            start_time = time.time()
            result = test_sarvam_chat(prompt=test_prompt)
            latency = time.time() - start_time
            
        if result["status"] == "success":
            st.success(f" Connected successfully in {latency:.2f} seconds!")
            
            st.markdown(
                f"""
                <div class="custom-card">
                    <div style="font-weight: 600; color: #475569; margin-bottom: 0.5rem;">
                        Response from Sarvam AI ({result['model']}):
                    </div>
                    <div class="response-box">
                        {result['response']}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.error(f"❌ Connection failed: {result.get('error')}")
            st.info("Please verify your internet connection and ensure your `SARVAM_API_KEY` has active chat credits.")
