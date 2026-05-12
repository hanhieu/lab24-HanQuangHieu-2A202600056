# AI Prompts Used in Lab 24

This document logs all AI prompts used during development for academic integrity purposes.

## Phase A: RAGAS Evaluation

### Test Set Generation Prompt
```
Generate synthetic test questions from the provided documents with the following distribution:
- 50% simple (single-hop) questions
- 25% reasoning (multi-step inference) questions  
- 25% multi-context (cross-document) questions

Each question should include:
- The question text
- Ground truth answer
- Relevant context chunks
- Evolution type classification
```

### RAGAS Evaluation Prompt
```
Evaluate the RAG pipeline responses using RAGAS metrics:
- Faithfulness: How well the answer is grounded in the context
- Answer Relevancy: How relevant the answer is to the question
- Context Precision: How relevant the retrieved context is
- Context Recall: How much of the ground truth is covered in context
```

## Phase B: LLM-as-Judge & Calibration

### Pairwise Judge Prompt
```
You are an impartial evaluator. Compare two answers to the same question.

Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}

Rate based on:
- Factual accuracy
- Relevance to question
- Conciseness

Output JSON only:
{"winner": "A" or "B" or "tie", "reason": "..."}
```

### Absolute Scoring Prompt
```
Score the answer on 4 dimensions, each 1-5 scale:

1. Factual accuracy (1=many errors, 5=fully accurate)
2. Relevance (1=off-topic, 5=directly answers)
3. Conciseness (1=verbose, 5=appropriately brief)
4. Helpfulness (1=unclear, 5=actionable)

Question: {question}
Answer: {answer}

Output JSON only:
{"accuracy": int, "relevance": int, "conciseness": int, "helpfulness": int, "overall": float}
```

## Phase C: Guardrails Stack

### Topic Validator Prompt
```
Is this question about one of these topics: {allowed_topics}?
Question: {text}
Answer YES or NO only.
```

### Llama Guard 3 Prompt
```
Built-in Llama Guard 3 model for safety classification.
No custom prompt - uses model's default safety classification.
```

## Phase D: Blueprint Document

### SLO Definition
No AI prompts used - manual documentation based on requirements.

### Architecture Diagram
No AI prompts used - manual ASCII diagram creation.

### Alert Playbook
No AI prompts used - manual incident response procedures.

### Cost Analysis
No AI prompts used - manual cost calculations based on API pricing.

## Notes

- All code was reviewed and understood before committing
- Mock data was generated for demonstration purposes where actual API calls were not feasible
- All implementations follow the Lab 24 requirements document specifications
- Academic integrity maintained by logging all AI-assisted development
