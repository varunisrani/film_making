"""
Utility functions for interacting with LLM APIs (OpenAI and Google Gemini).
"""
import os
import json
import time
from typing import Dict, Any, List, Optional, Union

import openai
import google.generativeai as genai
from dotenv import load_dotenv

# Import logging utilities
from utils.logging_utils import log_api_call

# Load environment variables
load_dotenv()

# Configure API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def call_openai_gpt(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    model: str = "gpt-4.1-mini",
    temperature: float = 0.7,
    max_tokens: int = 12000,
    json_mode: bool = False
) -> str:
    """Call the OpenAI GPT API.
    
    Args:
        prompt: The user prompt to send to the API
        system_message: The system message to set the context
        model: The model to use
        temperature: The temperature parameter for generation
        max_tokens: The maximum number of tokens to generate
        json_mode: Whether to request JSON output
        
    Returns:
        The generated text response
    """
    messages = [
        {"role": "system", "content": system_message},
        {"role": "user", "content": prompt}
    ]
    
    response_format = {"type": "json_object"} if json_mode else None
    
    start_time = time.time()
    error = None
    response_text = ""
    
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )
        response_text = response.choices[0].message.content
        status = "success"
    except Exception as e:
        error = str(e)
        status = "error"
        raise
    finally:
        duration = time.time() - start_time
        
        # Log the API call
        log_api_call(
            provider="openai",
            model=model,
            prompt_length=len(prompt) + len(system_message),
            response_length=len(response_text),
            duration=duration,
            status=status,
            error=error,
            metadata={
                "temperature": temperature,
                "max_tokens": max_tokens,
                "json_mode": json_mode
            }
        )
    
    return response_text

def call_gemini_pro(
    prompt: str,
    system_message: str = "You are a helpful assistant.",
    temperature: float = 0.7,
    max_tokens: int = 12000,
    json_mode: bool = False
) -> str:
    """Call the Google Gemini Pro API.
    
    Args:
        prompt: The user prompt to send to the API
        system_message: The system message to set the context
        temperature: The temperature parameter for generation
        max_tokens: The maximum number of tokens to generate
        json_mode: Whether to request structured JSON output
        
    Returns:
        The generated text response
    """
    model_name = "gemini-2.5-pro-preview-03-25"
    model = genai.GenerativeModel(
        model_name=model_name,
        generation_config={
            "temperature": temperature,
            "max_output_tokens": max_tokens,
        }
    )
    
    # Combine system message and prompt
    full_prompt = f"{system_message}\n\n{prompt}"
    
    if json_mode:
        full_prompt += "\n\nPlease format your response as a valid JSON object."
    
    start_time = time.time()
    error = None
    response_text = ""
    
    try:
        response = model.generate_content(full_prompt)
        response_text = response.text
        status = "success"
    except Exception as e:
        error = str(e)
        status = "error"
        raise
    finally:
        duration = time.time() - start_time
        
        # Log the API call
        log_api_call(
            provider="gemini",
            model=model_name,
            prompt_length=len(full_prompt),
            response_length=len(response_text),
            duration=duration,
            status=status,
            error=error,
            metadata={
                "temperature": temperature,
                "max_tokens": max_tokens,
                "json_mode": json_mode
            }
        )
    
    return response_text

def parse_json_response(response: str) -> Dict[str, Any]:
    """Parse a JSON response from an LLM.
    
    Args:
        response: The response string from the LLM
        
    Returns:
        The parsed JSON object
        
    Raises:
        ValueError: If the response cannot be parsed as JSON
    """
    # Try to extract JSON if it's wrapped in markdown code blocks
    if "```json" in response:
        start = response.find("```json") + 7
        end = response.find("```", start)
        json_str = response[start:end].strip()
    elif "```" in response:
        start = response.find("```") + 3
        end = response.find("```", start)
        json_str = response[start:end].strip()
    else:
        json_str = response
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {response}")