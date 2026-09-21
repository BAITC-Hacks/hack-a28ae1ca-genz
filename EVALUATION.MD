# Evaluation Criteria

Evaluate the implementation against the following criteria.

## Functional Correctness — 40%

The application:

- loads `messages.txt`;
- processes all five messages;
- produces exactly one category per message;
- uses only:
  - `справка`
  - `жалоба`
  - `другое`
- produces a Russian draft response for every message.

Expected classification:

| # | Category |
|---|---|
| 1 | справка |
| 2 | жалоба |
| 3 | другое |
| 4 | жалоба |
| 5 | справка |

## Reliability — 20%

The application:

- validates classifier output;
- handles malformed LLM responses;
- handles low confidence;
- handles empty input;
- does not crash because memory is missing;
- does not expose API secrets.

## Agent Architecture — 20%

The implementation should clearly demonstrate:

- classification;
- routing;
- tools or tool-like actions;
- memory;
- quality control.

Do not reward complexity by itself.

A smaller deterministic implementation is preferable to an unnecessarily complex framework.

## User Experience — 10%

CLI output should be:

- readable;
- concise;
- understandable;
- in Russian.

## Code Quality — 10%

Check:

- type hints;
- sensible function boundaries;
- minimal dependencies;
- clear naming;
- no dead code;
- no unnecessary frameworks;
- no hard-coded secrets.

## Anti-Criteria

The solution should not receive additional credit for:

- number of files;
- number of agents;
- number of LLM calls;
- use of LangChain;
- use of LangGraph;
- use of vector databases;
- unnecessary infrastructure.

The goal is a reliable small agent, not a large architecture.