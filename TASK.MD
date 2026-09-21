# Task: Build the Hackathon Solution

Build the complete solution for the hackathon task **"Классификатор обращений"**.

## Context

Track:

**Агентные системы**

Task:

**Классификатор обращений**

The task requires a script that reads five predefined Russian messages and prints:

- category: `справка`, `жалоба`, or `другое`;
- one draft response in Russian.

The organizers explicitly allow either rules or one LLM call.

## Goal

Build a compact but polished solution that demonstrates:

- classification;
- structured LLM output if LLM is used;
- routing;
- tools;
- lightweight memory;
- quality control;
- safe fallback.

Do not overengineer.

## Required Input

Create `messages.txt` with exactly:

```text
Как получить справку о месте учёбы?
В столовой очередь, еда холодная.
Хочу записаться на консультацию завтра.
Пропал Wi-Fi в корпусе B.
Где парковка для гостей?
```

## Expected Categories

```text
1 → справка
2 → жалоба
3 → другое
4 → жалоба
5 → справка
```

## Implementation

First inspect the repository.

Then implement the smallest architecture that satisfies `AGENTS.md`.

Prefer:

```text
loader
→ classifier
→ validation
→ router
→ response
→ quality check
→ memory
```

If using an LLM:

- use one call per message;
- request structured output;
- validate the result;
- constrain the category;
- use a confidence threshold;
- implement a safe fallback.

Do not use RAG.

Do not use a vector database.

Do not use multi-agent orchestration unless it materially improves the required behavior.

## Tools

Implement simple tools for:

```text
справка
жалоба
другое
```

Tools should prepare responses or records, not pretend to perform real external university actions.

## Memory

Implement lightweight JSON memory if practical.

It should not prevent the application from running when memory is missing or malformed.

## Quality Control

Validate every result before printing.

Invalid category:

```text
другое
```

Missing response:

```text
Не удалось сформировать ответ. Пожалуйста, уточните обращение.
```

Low confidence:

```text
другое
```

## Tests

Add tests for the five required messages.

Also test:

- irrelevant message;
- empty input;
- malformed classifier output;
- low confidence;
- memory failure.

## README

Write a concise README containing:

- project description;
- installation;
- configuration;
- launch command;
- architecture;
- sample output.

Do not overstate capabilities.

## Final Verification

Before finishing:

```text
- install dependencies
- run tests
- run the CLI
- verify all 5 required classifications
- verify no secrets are committed
- inspect git diff
```

Fix any issues found.

Do not stop after creating a rough prototype. Deliver a clean, runnable repository.