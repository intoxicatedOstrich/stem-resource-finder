import os
import json
from openai import OpenAI
from typing import Dict


class LLMProblemAnalyzer:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def analyze_problem(self, problem_text: str) -> Dict:
        prompt = f"""
You are an expert STEM educator. Analyze this problem by first solving it completely, then creating a dynamic learning progression.

PROBLEM: {problem_text}

STEP 1 - SOLVE THE PROBLEM:
First, work through the complete solution step-by-step. Identify every technique, concept, and sub-skill required.

STEP 2 - TECHNIQUE ANALYSIS:
For each technique identified:
- Rate its complexity within the subject domain (1-10)
- Determine prerequisite knowledge needed
- Assess if it needs further breakdown

STEP 3 - DYNAMIC PROGRESSION:
Based on the techniques needed, determine how many learning levels are required (typically 2-6 levels).
Create a progression where each level introduces 1-2 key techniques in logical order.

Return a structured JSON response:
{{
    "problem_solution": {{
        "complete_solution": "Step-by-step solution showing all work...",
        "techniques_used": [
            {{
                "name": "integration by parts",
                "complexity": 7,
                "required_for": "handling x² with trigonometric functions",
                "prerequisites": ["basic integration", "product rule for derivatives"]
            }}
        ]
    }},
    "problem_analysis": {{
        "subject": "calculus",
        "overall_difficulty": 8,
        "complexity_factors": ["multiple techniques combined", "trigonometric identities", "algebraic manipulation"],
        "estimated_levels_needed": 4,
        "reasoning": "This problem combines polynomial and trigonometric integration requiring multiple advanced techniques..."
    }},
    "learning_progression": [
        {{
            "level": 1,
            "title": "Foundation Level Name",
            "difficulty": 3,
            "techniques_introduced": ["technique1", "technique2"],
            "example_problems": ["problem1", "problem2"],
            "search_queries": ["targeted search query 1", "targeted search query 2"],
            "why_this_level": "Explains the logical progression reason",
            "builds_toward": "Next level preparation"
        }}
    ]
}}

Make the progression adaptive - use as many levels as needed based on the actual complexity analysis."""

        response = self.client.chat.completions.create(
            model="gpt-5",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )

        return json.loads(response.choices[0].message.content)