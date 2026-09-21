# ROADMAP

## Milestone v1 — LLM Integration

### Phase 1: LLM Integration with Gemini
**Goal:** Add optional LLM-based classification and response generation using Google Gemini API, with rule-based/template fallbacks.
**Success Criteria:**
1. `python main.py` works without API key (rule-based classification)
2. `python main.py --llm` works with `GEMINI_API_KEY` set
3. LLM failure gracefully falls back to rule-based classifier
4. All 5 required messages classify correctly in both modes
5. Response generation works in both modes (template and LLM)

**Requirements:** ALL-01, ALL-02, ALL-03, ALL-04, ALL-05

### Phase 2: Testing & Validation
**Goal:** Ensure all test cases pass, including edge cases and LLM fallback scenarios.
**Success Criteria:**
1. All 21 existing tests pass
2. New LLM-specific tests pass (with mocks)
3. Manual verification of all 5 required messages
4. Edge cases handled (empty input, invalid API key, network failure)

**Requirements:** ALL-06
