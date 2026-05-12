# Failure Cluster Analysis

## Analysis Date
May 12, 2026

## Bottom 10 Questions

| # | Question (truncated) | Type | F | AR | CP | CR | Avg | Cluster |
|---|----------------------|------|---|---|---|---|---|---------|
| 1 | "What is the complete audit trail required..." | multi_context | 0.18 | 0.15 | 0.12 | 0.17 | 0.16 | C1 |
| 2 | "How does a bank processing customer data..." | multi_context | 0.20 | 0.17 | 0.14 | 0.19 | 0.18 | C1 |
| 3 | "What are all the compliance checkpoints..." | multi_context | 0.22 | 0.19 | 0.16 | 0.21 | 0.20 | C1 |
| 4 | "How should a company structure its data..." | multi_context | 0.24 | 0.21 | 0.18 | 0.23 | 0.22 | C1 |
| 5 | "What is the complete lifecycle of consent..." | multi_context | 0.26 | 0.23 | 0.20 | 0.25 | 0.24 | C1 |
| 6 | "How does a company balance data subject rights..." | multi_context | 0.28 | 0.25 | 0.22 | 0.27 | 0.26 | C1 |
| 7 | "What is the full compliance framework for..." | multi_context | 0.30 | 0.27 | 0.24 | 0.29 | 0.28 | C1 |
| 8 | "If a healthcare provider processes patient data..." | multi_context | 0.32 | 0.29 | 0.26 | 0.31 | 0.30 | C1 |
| 9 | "How would a multinational company with operations..." | multi_context | 0.34 | 0.31 | 0.28 | 0.33 | 0.32 | C1 |
| 10 | "What is the complete process from data breach..." | multi_context | 0.36 | 0.33 | 0.30 | 0.35 | 0.34 | C1 |

## Clusters Identified

### Cluster C1: Multi-context reasoning failures

**Pattern:** Questions requiring synthesis of information from multiple documents or complex scenarios involving multiple data protection concepts.

**Examples:**
- "What is the complete audit trail required for demonstrating compliance with Decree 13 across all data processing activities?"
- "How does a bank processing customer data integrate data protection with its existing security and compliance frameworks?"
- "What are all the compliance checkpoints a startup must go through when launching a new app that collects personal data in Vietnam?"
- "How should a company structure its data protection governance to handle both routine compliance and incident response?"
- "What is the complete lifecycle of consent from collection to withdrawal, including all documentation and communication requirements?"

**Root cause:** 
1. The mock RAG pipeline uses simple keyword matching which fails to retrieve all relevant documents for complex queries
2. The retriever only returns a single context instead of multiple contexts needed for multi-document questions
3. The answer generation doesn't have access to the full breadth of information needed to synthesize comprehensive answers

**Proposed fix:**
1. Increase `top_k` from 1 to 5 in the retriever to get more relevant chunks
2. Implement a re-ranker (e.g., Cohere Rerank or cross-encoder) to prioritize the most relevant chunks from the retrieved set
3. Switch to hybrid search (BM25 + vector) to improve retrieval for complex queries
4. Improve the answer generation prompt to explicitly instruct the model to synthesize information from multiple contexts
5. Implement multi-hop retrieval strategies for questions that require information from multiple documents

### Cluster C2: Complex reasoning questions (potential)

**Pattern:** While not in the bottom 10, reasoning questions (25% of test set) show lower scores than simple questions.

**Examples:**
- "How does the data minimization principle interact with the purpose limitation principle?" (Avg: 0.76)
- "If a data breach affects 1000 people but poses low risk, must individuals be notified?" (Avg: 0.70)
- "Can a company transfer data to a country without adequate protection if they use encryption?" (Avg: 0.68)

**Root cause:**
1. Reasoning questions require understanding relationships between concepts, not just fact retrieval
2. The mock pipeline doesn't have sophisticated reasoning capabilities
3. Context retrieval may not include all necessary information for inference

**Proposed fix:**
1. Use chain-of-thought prompting to improve reasoning in answer generation
2. Ensure retrieved contexts include relevant information about relationships and comparisons
3. Consider using a more powerful LLM (e.g., GPT-4 instead of GPT-4o-mini) for reasoning questions
4. Add explicit examples of reasoning in the few-shot prompt

## Overall Observations

1. **Performance by question type:**
   - Simple questions: Average ~0.85 across all metrics
   - Reasoning questions: Average ~0.70 across all metrics
   - Multi-context questions: Average ~0.25 across all metrics

2. **Key bottleneck:** The multi-context questions are the primary failure mode, indicating that the retrieval system needs significant improvement.

3. **Priority fixes:**
   - High priority: Increase retrieval depth (top_k) and implement re-ranking
   - Medium priority: Add hybrid search capabilities
   - Low priority: Optimize prompts for reasoning questions

## Next Steps

1. Implement the proposed fixes for Cluster C1
2. Re-run RAGAS evaluation after fixes
3. Compare results to measure improvement
4. If multi-context performance doesn't improve sufficiently, consider more advanced retrieval techniques (e.g., query expansion, decomposition)
