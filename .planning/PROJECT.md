# PROJECT

## What This Is

A CLI agent that classifies Russian-language student messages into three categories (справка, жалоба, другое) and generates draft responses. Currently uses rule-based classification; adding LLM capabilities via Google Gemini.

## Core Value

Classify student messages accurately and generate appropriate responses in Russian.

## Constraints

- No heavy frameworks (LangChain, LangGraph, LlamaIndex, vector DBs)
- No RAG or web search
- API keys via env vars only
- All responses in Russian
- Short, polite, neutral responses
- No hallucinated facts

## Requirements

### Validated

- ✓ Rule-based classification works for 5 required messages
- ✓ Template-based response generation works
- ✓ Memory persistence works

### Active

- [ ] LLM-based classification with Gemini
- [ ] LLM-based response generation
- [ ] `--llm` CLI flag
- [ ] Graceful fallback on LLM failure

### Out of Scope

- Heavy frameworks
- Multiple LLM providers
- Streaming responses

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| Use Google Gemini | Free tier, good performance | Accepted |
| Rule-based as fallback | No API dependency | Accepted |
| Single LLM call per message | Meets constraints | Accepted |

---
*Last updated: 2026-09-21 after initialization*
