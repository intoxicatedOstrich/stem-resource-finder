# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Architecture

This is a CLI tool that creates learning progressions for STEM problems using GPT-5 analysis and web search. The core workflow is:

1. **Problem Analysis**: GPT-5 analyzes difficulty and generates a 4-level learning progression
2. **Resource Search**: Serper API searches for educational content at each difficulty level
3. **Result Ranking**: Educational sites are ranked by domain authority and content relevance
4. **Formatted Output**: Rich CLI formatting displays the learning ladder with resources

### Key Components

- `problem_ladder.py` - Main CLI orchestrating the full workflow
- `modules/llm_analyzer.py` - GPT-5 integration for intelligent problem analysis
- `modules/search_engine.py` - Serper API wrapper with educational site filtering
- `modules/problem_ranker.py` - Multi-factor ranking algorithm for search results
- `utils/formatters.py` - Rich-based CLI output formatting

### Critical Configuration

The tool requires two APIs configured in `.env`:
- `OPENAI_API_KEY` - For GPT-5 problem analysis (core functionality)
- `SERPER_API_KEY` - For educational resource search

The `config.json` contains:
- Educational domain preferences and scoring weights
- Subject-specific keywords and difficulty markers
- GPT model settings and search parameters

### GPT-5 Integration Strategy

The LLM analyzer uses structured JSON prompts to generate learning progressions. Key prompt engineering principles:
- Request specific JSON structure with problem analysis and 4-level progression
- Include reasoning for difficulty assessment and concept introduction
- Generate targeted search queries for each level
- Emphasize educational context and step-by-step learning

### Search and Ranking Logic

Search results are ranked using weighted scoring:
- Domain Authority (30%): .edu sites and known educational platforms
- Content Relevance (40%): Keyword matching for concepts and solution indicators
- Difficulty Match (30%): Title/snippet analysis for appropriate complexity

Preferred domains include Khan Academy, MIT, Stanford, Brilliant, and other educational sites defined in `config.json`.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env with your API keys

# Run the tool
python problem_ladder.py "your STEM problem here"

# Example usage
python problem_ladder.py "∫ sin²(x)cos³(x) dx"
python problem_ladder.py "solve x² + 5x + 6 = 0" --levels 3
```

## Implementation Status

Currently in development phase with basic structure established. Core modules need implementation based on specifications in `IMPLEMENTATION_PLAN.md`. The project follows a modular design where each component can be developed and tested independently before integration.