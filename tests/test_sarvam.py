"""
Unit and integration tests for Sarvam Client.
"""

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure parent directory is in python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from sarvam_client import get_api_key, chat_completion, DEFAULT_CHAT_MODEL


class TestSarvamClient(unittest.TestCase):

    def test_missing_api_key_raises(self):
        """When API key is None, chat_completion should raise ValueError."""
        with patch("sarvam_client.get_api_key", return_value=None):
            with self.assertRaises(ValueError) as ctx:
                chat_completion(messages=[{"role": "user", "content": "hello"}])
            self.assertIn("SARVAM_API_KEY is not set", str(ctx.exception))

    @patch("requests.post")
    def test_chat_completion_mock(self, mock_post):
        """Verify chat_completion sends correct headers and payload."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "choices": [
                {
                    "message": {
                        "content": "नमस्ते! मैं आपकी सहायता कर सकता हूँ।"
                    }
                }
            ]
        }
        mock_post.return_value = mock_response

        with patch("sarvam_client.get_api_key", return_value="test_mock_key_xyz"):
            reply = chat_completion(
                messages=[{"role": "user", "content": "नमस्ते"}]
            )
            self.assertEqual(reply, "नमस्ते! मैं आपकी सहायता कर सकता हूँ।")

            # Check call args
            mock_post.assert_called_once()
            args, kwargs = mock_post.call_args
            self.assertEqual(args[0], "https://api.sarvam.ai/v1/chat/completions")
            self.assertEqual(kwargs["headers"]["api-subscription-key"], "test_mock_key_xyz")
            self.assertEqual(kwargs["json"]["model"], DEFAULT_CHAT_MODEL)


if __name__ == "__main__":
    unittest.main()
