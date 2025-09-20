import os
import json
from openai import OpenAI
from typing import Dict


class LLMProblemAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_problem(self, problem_text: str) -> Dict:
        prompt = f"""
You are an expert STEM educator analyzing a student's problem to create a learning progression.

PROBLEM: {problem_text}

Your task:
1. Identify the subject area and key concepts
2. Rate difficulty (1-10) with reasoning
3. Create a 4-level learning ladder from basic to the target problem
4. Generate specific search queries to find practice problems for each level

Return a structured JSON response:
{{
    "problem_analysis": {{
        "subject": "calculus",
        "difficulty": 8,
        "concepts": ["integration by parts", "trigonometric substitution"],
        "prerequisite_knowledge": ["basic integration", "trigonometry"],
        "reasoning": "This problem requires advanced integration techniques..."
    }},
    "learning_progression": [
        {{
            "level": 1,
            "title": "Basic Polynomial Integration",
            "difficulty": 3,
            "concepts_introduced": ["power rule"],
            "example_problem": "∫ x^2 dx",
            "search_queries": [
                "basic polynomial integration examples step by step",
                "power rule integration practice problems with solutions"
            ],
            "why_this_level": "Establishes fundamental integration skills before adding complexity"
        }},
        {{
            "level": 2,
            "title": "Simple Trigonometric Integration",
            "difficulty": 5,
            "concepts_introduced": ["basic trig integrals"],
            "example_problem": "∫ sin(x) dx",
            "search_queries": [
                "basic trigonometric integration examples",
                "sin cos integration practice problems"
            ],
            "why_this_level": "Introduces trigonometric functions in integration context"
        }},
        {{
            "level": 3,
            "title": "Trigonometric Powers",
            "difficulty": 6,
            "concepts_introduced": ["trig identities", "power reduction"],
            "example_problem": "∫ sin²(x) dx",
            "search_queries": [
                "trigonometric power integration examples",
                "sin squared cos squared integration techniques"
            ],
            "why_this_level": "Builds toward handling powers of trig functions"
        }},
        {{
            "level": 4,
            "title": "Advanced Trigonometric Integration",
            "difficulty": 8,
            "concepts_introduced": ["integration by parts with trig", "substitution"],
            "example_problem": "∫ sin²(x)cos³(x) dx",
            "search_queries": [
                "advanced trigonometric integration examples",
                "sin squared cos cubed integration solution"
            ],
            "why_this_level": "Target problem - combines all previous concepts"
        }}
    ]
}}
"""

        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)