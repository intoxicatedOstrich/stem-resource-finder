# STEM Resource Finder - Implementation Plan

## Project Overview
A CLI tool that accepts STEM problem text input, uses GPT-5 to analyze difficulty and create a learning progression, then searches for easier practice problems using Serper API.

## Architecture Design

### Core Components
```
stem-resource-finder/
├── problem_ladder.py           # Main CLI application
├── modules/
│   ├── __init__.py
│   ├── llm_analyzer.py        # GPT-5 problem analysis
│   ├── search_engine.py       # Serper API integration
│   └── problem_ranker.py      # Result ranking/filtering
├── utils/
│   ├── __init__.py
│   └── formatters.py          # Output formatting helpers
├── config.json                # Search preferences & domains
├── requirements.txt
├── .env.example
└── README.md
```

## Dependencies
- `openai>=1.0.0` - GPT-5 API integration
- `requests>=2.31.0` - HTTP requests for Serper API
- `python-dotenv>=1.0.0` - Environment variable management
- `beautifulsoup4>=4.12.2` - HTML parsing for search results
- `rich>=13.0.0` - Enhanced CLI output formatting

## Environment Configuration
```env
OPENAI_API_KEY=your_openai_api_key_here
SERPER_API_KEY=your_serper_api_key_here
GPT_MODEL=gpt-4-turbo  # Update to gpt-5 when available
MAX_SEARCH_RESULTS=10
DIFFICULTY_LEVELS=4
DEBUG=false
```

## Module Specifications

### 1. LLM Analyzer (`modules/llm_analyzer.py`)

**Purpose**: Use GPT-5 to analyze STEM problems and generate learning progressions

**Key Methods**:
```python
class LLMProblemAnalyzer:
    def analyze_problem(self, problem_text: str) -> Dict
    def _build_analysis_prompt(self, problem_text: str) -> str
    def _parse_structured_response(self, response: str) -> Dict
    def _validate_analysis_result(self, result: Dict) -> bool
```

**GPT-5 Prompt Strategy**:
```python
ANALYSIS_PROMPT = """
You are an expert STEM educator analyzing a student's problem to create a learning progression.

PROBLEM: {problem_text}

Your task:
1. Identify the subject area and key concepts
2. Rate difficulty (1-10) with reasoning
3. Create a 4-level learning ladder from basic to the target problem
4. Generate specific search queries to find practice problems for each level

Return a structured JSON response:
{
    "problem_analysis": {
        "subject": "calculus",
        "difficulty": 8,
        "concepts": ["integration by parts", "trigonometric substitution"],
        "prerequisite_knowledge": ["basic integration", "trigonometry"],
        "reasoning": "This problem requires advanced integration techniques..."
    },
    "learning_progression": [
        {
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
        },
        {
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
        },
        {
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
        },
        {
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
        }
    ]
}
"""
```

### 2. Search Engine (`modules/search_engine.py`)

**Purpose**: Interface with Serper API to find educational resources

**Key Methods**:
```python
class SerperSearchEngine:
    def search_for_resources(self, query: str, level: int) -> List[Dict]
    def _build_search_params(self, query: str) -> Dict
    def _filter_educational_sites(self, results: List) -> List
    def _extract_result_metadata(self, result: Dict) -> Dict
```

**Search Strategy**:
- Prefer educational domains (edu, org, known educational sites)
- Include terms like "examples", "step by step", "practice problems"
- Filter results based on content relevance and domain authority

### 3. Problem Ranker (`modules/problem_ranker.py`)

**Purpose**: Rank and filter search results by relevance and educational value

**Key Methods**:
```python
class ProblemRanker:
    def rank_results(self, results: List, target_difficulty: int, concepts: List) -> List
    def _calculate_domain_score(self, url: str) -> float
    def _calculate_content_relevance(self, result: Dict, concepts: List) -> float
    def _calculate_difficulty_match(self, result: Dict, target_difficulty: int) -> float
```

**Ranking Criteria**:
1. **Domain Authority** (30%): Educational sites ranked higher
2. **Content Relevance** (40%): Matches concepts and includes solution keywords
3. **Difficulty Match** (30%): Title/snippet suggests appropriate difficulty level

### 4. CLI Formatter (`utils/formatters.py`)

**Purpose**: Create beautiful, readable CLI output using Rich library

**Key Methods**:
```python
class LearningLadderFormatter:
    def format_analysis_summary(self, analysis: Dict) -> str
    def format_learning_progression(self, progression: List) -> str
    def format_search_results(self, results: List, level: int) -> str
    def format_error_message(self, error: str) -> str
```

## Main Application Flow (`problem_ladder.py`)

```python
def main():
    # 1. Parse command line arguments
    args = parse_arguments()

    # 2. Initialize components
    analyzer = LLMProblemAnalyzer()
    search_engine = SerperSearchEngine()
    ranker = ProblemRanker()
    formatter = LearningLadderFormatter()

    # 3. Analyze the problem with GPT-5
    analysis = analyzer.analyze_problem(args.problem_text)

    # 4. Display analysis summary
    print(formatter.format_analysis_summary(analysis))

    # 5. For each level in the learning progression:
    for level_info in analysis['learning_progression']:
        # Search for resources
        raw_results = search_engine.search_for_resources(
            level_info['search_queries'][0],
            level_info['level']
        )

        # Rank and filter results
        ranked_results = ranker.rank_results(
            raw_results,
            level_info['difficulty'],
            level_info['concepts_introduced']
        )

        # Display formatted results
        print(formatter.format_search_results(ranked_results, level_info['level']))
```

## Configuration (`config.json`)

```json
{
  "educational_domains": [
    "khanacademy.org",
    "brilliant.org",
    "mit.edu",
    "stanford.edu",
    "coursera.org",
    "edx.org",
    "tutorial.math.lamar.edu",
    "mathisfun.com",
    "purplemath.com",
    "wolframalpha.com",
    "symbolab.com",
    "mathway.com"
  ],
  "domain_scores": {
    "edu": 1.0,
    "org": 0.8,
    "khanacademy.org": 1.0,
    "brilliant.org": 0.9,
    "mit.edu": 1.0,
    "stanford.edu": 1.0
  },
  "search_preferences": {
    "include_solutions": true,
    "prefer_worked_examples": true,
    "max_results_per_level": 5,
    "educational_keywords": [
      "step by step",
      "worked example",
      "practice problem",
      "solution",
      "tutorial",
      "explanation"
    ]
  },
  "gpt_settings": {
    "temperature": 0.3,
    "max_tokens": 2000,
    "response_format": { "type": "json_object" }
  }
}
```

## Example Usage

```bash
# Basic usage
python problem_ladder.py "∫ sin²(x)cos³(x) dx"

# With custom difficulty levels
python problem_ladder.py "solve x² + 5x + 6 = 0" --levels 3

# Verbose output
python problem_ladder.py "find the limit as x approaches 0 of sin(x)/x" --verbose

# Export results
python problem_ladder.py "prove that √2 is irrational" --export results.json
```

## Expected Output Format

```
═══ Problem Analysis ═══
Subject: Calculus (Trigonometric Integration)
Difficulty: 8/10
Key Concepts: Integration by parts, trigonometric identities, power reduction
Prerequisites: Basic integration, trigonometry fundamentals

Reasoning: This problem requires advanced integration techniques combining
trigonometric identities with substitution methods.

═══ Learning Ladder ═══

┌─ Level 1 (Difficulty 3/10): Basic Polynomial Integration ─┐
│ Example: ∫ x² dx                                          │
│ Why: Establishes fundamental integration skills           │
│                                                           │
│ 📚 Resources:                                            │
│ 1. Khan Academy: Power Rule Integration                   │
│    https://khanacademy.org/math/calculus-1/...           │
│    ★★★★★ Comprehensive tutorial with examples             │
│                                                           │
│ 2. Paul's Online Math: Basic Integration                  │
│    https://tutorial.math.lamar.edu/...                   │
│    ★★★★☆ Step-by-step worked examples                     │
└───────────────────────────────────────────────────────────┘

┌─ Level 2 (Difficulty 5/10): Simple Trigonometric Integration ─┐
│ Example: ∫ sin(x) dx                                          │
│ New Concepts: Basic trigonometric integrals                   │
│ Why: Introduces trigonometric functions in integration        │
│                                                               │
│ 📚 Resources:                                                │
│ 1. MIT OpenCourseWare: Trig Integration                       │
│    https://ocw.mit.edu/courses/...                           │
│    ★★★★★ Rigorous mathematical treatment                       │
└───────────────────────────────────────────────────────────────┘

... [continues for levels 3 and 4] ...
```

## Error Handling Strategy

1. **API Failures**: Graceful fallback to cached responses or simplified analysis
2. **Invalid Input**: Clear error messages with suggestions for valid input
3. **Rate Limiting**: Implement exponential backoff for API calls
4. **Network Issues**: Retry logic with user feedback

## Testing Strategy

1. **Unit Tests**: Each module tested independently
2. **Integration Tests**: End-to-end workflow testing
3. **Example Problems**: Curated set of test problems across subjects
4. **Performance Tests**: API response time and accuracy validation

## Future Enhancements

1. **Image Support**: Add OCR capability for screenshot input
2. **Caching**: Store GPT-5 analyses to reduce API costs
3. **Progress Tracking**: User accounts and learning progress
4. **Export Options**: PDF, Markdown, or interactive HTML reports
5. **Web Interface**: Browser-based version of the tool
6. **Integration**: Connect with existing learning platforms

## Implementation Timeline

1. **Week 1**: Core modules (LLM analyzer, search engine)
2. **Week 2**: CLI interface and formatting
3. **Week 3**: Result ranking and configuration
4. **Week 4**: Testing, documentation, and refinement

## Success Metrics

- Generates relevant learning progressions for 90%+ of STEM problems
- Finds high-quality educational resources (avg rating 4/5 stars)
- Response time under 10 seconds for complete analysis
- User satisfaction through progressive difficulty matching