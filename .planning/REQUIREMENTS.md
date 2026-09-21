# REQUIREMENTS

## v1 Requirements

### Classification
- [ ] **CLF-01**: LLM-based classification using Gemini API
- [ ] **CLF-02**: Structured output validation against Literal["справка", "жалоба", "другое"]
- [ ] **CLF-03**: Fallback to rule-based classifier on LLM failure
- [ ] **CLF-04**: Single LLM call per message (no RAG, no web search)

### Response Generation
- [ ] **RES-01**: LLM-based response generation using Gemini API
- [ ] **RES-02**: Response rules enforced (Russian, polite, no hallucinations)
- [ ] **RES-03**: Fallback to template responses on LLM failure

### CLI & Configuration
- [ ] **CLI-01**: `--llm` flag to enable LLM mode
- [ ] **CLI-02**: API key via `GEMINI_API_KEY` env var
- [ ] **CLI-03**: Graceful error handling for missing API key

### Testing
- [ ] **TST-01**: All existing tests pass
- [ ] **TST-02**: LLM tests with mocks
- [ ] **TST-03**: Edge case coverage (empty input, invalid API key)

## Out of Scope

- Heavy frameworks (LangChain, LlamaIndex, etc.)
- RAG or web search
- Multiple LLM providers
- Streaming responses
- Batch processing

## Traceability

| Requirement | Phase |
|-------------|-------|
| CLF-01 to CLF-04 | 1 |
| RES-01 to RES-03 | 1 |
| CLI-01 to CLI-03 | 1 |
| TST-01 to TST-03 | 2 |
