"""
Sarvam AI Client for Nidaan (निदान) AI Tutor.
Handles chat completions, Indian-language prompts, and API interaction.

Security:
- Never logs, prints, or exposes the SARVAM_API_KEY.
- Reads exclusively from environment variables populated via python-dotenv.
"""

import os
from typing import List, Dict, Optional, Any
import requests
from dotenv import load_dotenv, find_dotenv

# Load .env searching upward from current working directory
load_dotenv(find_dotenv(usecwd=True))

# Also load from sarvam.evm (user's preferred key file) — checks same dir and parent dirs
_evm_path = find_dotenv(filename="sarvam.evm", usecwd=True)
if _evm_path:
    load_dotenv(_evm_path, override=True)

SARVAM_CHAT_URL = "https://api.sarvam.ai/v1/chat/completions"
DEFAULT_CHAT_MODEL = "sarvam-105b"


def get_api_key() -> Optional[str]:
    """
    Retrieve Sarvam API key safely.
    Returns None if key is not found or empty.
    """
    key = os.getenv("SARVAM_API_KEY")
    if not key or key.strip() == "" or key.strip() == "your_key_here":
        return None
    return key.strip()


def chat_completion(
    messages: List[Dict[str, str]],
    model: str = DEFAULT_CHAT_MODEL,
    temperature: float = 0.3,
    max_tokens: int = 500,
    timeout: int = 25,
) -> str:
    """
    Send chat messages to Sarvam AI and return assistant text response.
    
    Args:
        messages: List of message dicts: [{'role': 'user'|'system'|'assistant', 'content': '...'}]
        model: Sarvam model name (defaults to 'sarvam-105b')
        temperature: Sampling temperature (0.0 to 1.0)
        max_tokens: Maximum tokens in response
        timeout: Request timeout in seconds

    Returns:
        Generated text response from the model.
    """
    api_key = get_api_key()
    if not api_key:
        raise ValueError(
            "SARVAM_API_KEY is not set. Please create a .env file containing SARVAM_API_KEY=your_key_here."
        )

    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": api_key,
    }

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    try:
        response = requests.post(
            SARVAM_CHAT_URL,
            json=payload,
            headers=headers,
            timeout=timeout,
        )

        if response.status_code == 401 or response.status_code == 403:
            raise PermissionError(
                "Authentication failed with Sarvam AI. Please check that SARVAM_API_KEY in .env is valid."
            )
        elif response.status_code == 429:
            raise RuntimeError(
                "Sarvam AI rate limit reached. Please wait a moment and try again."
            )
        elif response.status_code != 200:
            raise RuntimeError(
                f"Sarvam AI API error (HTTP {response.status_code}): {response.text}"
            )

        data = response.json()
        choices = data.get("choices", [])
        if not choices:
            raise ValueError("No choices returned from Sarvam AI response.")

        content = choices[0].get("message", {}).get("content", "")
        return content.strip()

    except requests.exceptions.Timeout:
        raise TimeoutError("Sarvam AI request timed out. Please check your internet connection.")
    except requests.exceptions.ConnectionError:
        raise ConnectionError("Could not connect to Sarvam AI. Please check your network connection.")


def test_sarvam_chat(prompt: str = "नमस्ते! Nidaan AI Tutor test connection.") -> Dict[str, Any]:
    """
    Quick test helper function for verifying connectivity to Sarvam AI.
    
    Returns a dict with 'status', 'response', 'model', and optional 'error'.
    """
    try:
        reply = chat_completion(
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        return {
            "status": "success",
            "model": DEFAULT_CHAT_MODEL,
            "prompt": prompt,
            "response": reply,
        }
    except Exception as e:
        return {
            "status": "error",
            "model": DEFAULT_CHAT_MODEL,
            "prompt": prompt,
            "error": str(e),
        }


if __name__ == "__main__":
    import sys
    # Fix Windows console encoding for Hindi/emoji output
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    print("Testing Sarvam AI Connection...")
    result = test_sarvam_chat()
    if result["status"] == "success":
        print("[SUCCESS] Connected to Sarvam AI successfully!")
        print(f"Model: {result['model']}")
        print(f"Response: {result['response']}")
    else:
        print("[ERROR] Could not connect to Sarvam AI.")
        print(f"Details: {result['error']}")

