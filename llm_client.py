"""Shared Gemini LLM client for classification and response generation."""

import os
import json
from typing import Optional


def call_llm(prompt: str, system: str = "", timeout: int = 30) -> Optional[str]:
    """Call Google Gemini API with a prompt and optional system instruction.

    Args:
        prompt: The user prompt to send.
        system: Optional system instruction.
        timeout: Request timeout in seconds.

    Returns:
        The model's response text, or None on failure.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        contents = []
        if system:
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=f"System: {system}\n\nUser: {prompt}")]
            ))
        else:
            contents.append(types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)]
            ))

        config = types.GenerateContentConfig()
        if system:
            config.system_instruction = system

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )

        if response.text:
            return response.text.strip()
        return None

    except ImportError:
        raise ImportError("google-genai package not installed. Run: pip install google-genai")
    except Exception as e:
        print(f"LLM call failed: {e}")
        return None


def parse_json_response(text: str) -> Optional[dict]:
    """Parse a JSON response from the LLM.

    Handles common LLM output patterns like markdown code blocks.

    Args:
        text: Raw text response from LLM.

    Returns:
        Parsed JSON dict, or None if parsing fails.
    """
    if not text:
        return None

    cleaned = text.strip()

    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.startswith("```") and not in_block:
                in_block = True
                continue
            elif line.startswith("```") and in_block:
                break
            elif in_block:
                json_lines.append(line)
        cleaned = "\n".join(json_lines).strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None
