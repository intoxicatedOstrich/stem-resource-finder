#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from modules.llm_analyzer import LLMProblemAnalyzer

# Load environment variables
load_dotenv()

# Create analyzer
analyzer = LLMProblemAnalyzer()

# Test with a complex integration problem that needs breakdown
problem = "∫ x²sin³(x)cos²(x) dx"

print("Analyzing problem:", problem)
print("=" * 50)

try:
    result = analyzer.analyze_problem(problem)

    # Print the solution analysis
    solution = result["problem_solution"]
    print("COMPLETE SOLUTION:")
    print(solution["complete_solution"])
    print("\nTECHNIQUES IDENTIFIED:")
    for tech in solution["techniques_used"]:
        print(f"  • {tech['name']} (complexity: {tech['complexity']}/10)")
        print(f"    Required for: {tech['required_for']}")

    # Print the analysis
    analysis = result["problem_analysis"]
    print(f"\nANALYSIS:")
    print(f"Subject: {analysis['subject']}")
    print(f"Overall Difficulty: {analysis['overall_difficulty']}/10")
    print(f"Levels Needed: {analysis['estimated_levels_needed']}")
    print(f"Reasoning: {analysis['reasoning']}")

    print(f"\nLEARNING PROGRESSION ({len(result['learning_progression'])} levels):")
    for level in result["learning_progression"]:
        print(f"\n--- Level {level['level']}: {level['title']} ---")
        print(f"  Difficulty: {level['difficulty']}/10")
        print(f"  Techniques: {', '.join(level['techniques_introduced'])}")
        print(f"  Examples: {', '.join(level['example_problems'])}")
        print(f"  Why: {level['why_this_level']}")

except Exception as e:
    print(f"Error: {e}")