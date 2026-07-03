"""
AI Engine Module

This module sends genome analysis results to an LLM
(OpenAI, Ollama, etc.) and returns a professional
biological interpretation.
"""

import os
from openai import OpenAI


class AIEngine:
    """
    AI Engine for genome interpretation.
    """

    def __init__(self):

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY environment variable not found."
            )

        self.client = OpenAI(api_key=api_key)

    def generate_report(self, prompt):

        response = self.client.chat.completions.create(

            model="gpt-4.1-mini",

            messages=[
                {
                    "role": "system",
                    "content":
                    (
                        "You are an expert bioinformatician. "
                        "Interpret genome analysis results using "
                        "scientific language suitable for publication."
                    )
                },

                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.2,

            max_tokens=1500

        )

        return response.choices[0].message.content