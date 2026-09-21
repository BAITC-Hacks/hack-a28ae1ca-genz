# AGENTS.md

## Project

Hackathon project: "Классификатор обращений" (Request Classifier) for the "Агентные системы" track.

A small CLI agent that classifies Russian-language student messages into three categories and generates draft responses.

## Categories

- `справка` — information requests (locations, procedures, instructions)
- `жалоба` — complaints (problems, malfunctions, dissatisfaction)
- `другое` — everything else

## Expected Results for Required Messages

| # | Message | Category |
|---|---------|----------|
| 1 | Как получить справку о месте учёбы? | справка |
| 2 | В столовой очередь, еда холодная. | жалоба |
| 3 | Хочу записаться на консультацию завтра. | другое |
| 4 | Пропал Wi-Fi в корпусе B. | жалоба |
| 5 | Где парковка для гостей? | справка |

## Required Files

- `messages.txt` — 5 required messages exactly as specified
- `main.py` — entry point, run with `python main.py`
- `requirements.txt` — minimal dependencies only
- `README.md` — setup, architecture diagram, output example
- `.gitignore` — exclude `.env`, `__pycache__/`, `.venv/`, `memory.json`

## Architecture (Pipeline)

```
messages.txt → Input Loader → Classifier → Structured Result
    → Validation → Router → Response Generator
    → Quality Check → Memory → CLI Output
```

## Key Constraints

- **No heavy frameworks**: No LangChain, LangGraph, LlamaIndex, vector DBs, Kafka, Redis, Docker
- **No RAG or web search** — classification is local or via a single LLM call per message
- **Structured output only** if LLM is used — validate against `Literal["справка", "жалоба", "другое"]`
- **Safe fallbacks**: low confidence → `другое`; invalid LLM output → retry once or fallback
- **API keys via env vars only** — never commit secrets; provide `.env.example` if needed

## Response Rules

- All responses in Russian
- Short, polite, neutral, useful
- No hallucinated facts (no office numbers, URLs, names, hours)
- Phrasing like "Обращение подготовлено для передачи ответственному сотруднику" for complaints (no claims of actual submission)

## Quality Checks

Every output must pass:
- category ∈ {справка, жалоба, другое}
- response is non-empty, in Russian
- confidence between 0 and 1
- Never print None, null, {}, or invalid category

## Memory

- Store `{message, category, response}` in `memory.json`
- Create automatically if missing; recover if corrupted
- Not a dependency for basic operation

## Testing

Required test cases:
1. The 5 required messages → deterministic expected categories
2. Irrelevant input → fallback
3. Empty input → safe handling
4. Invalid LLM output → retry/fallback
5. Low confidence → `другое`
6. Missing/corrupted memory → no crash

## Engineering Style

- Simple functions, minimal classes
- Type hints on all functions
- Explicit error handling (no broad `except: pass`)
- Readable CLI output with clear formatting
- Keep total project small — understandable in minutes

## Commands

```bash
# Install
pip install -r requirements.txt

# Run
python main.py

# Test
python -m pytest tests/ -v
```
