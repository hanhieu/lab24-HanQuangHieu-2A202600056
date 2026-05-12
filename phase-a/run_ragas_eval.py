"""
Phase A.2 - Run RAGAS 4 Metrics
Evaluate RAG pipeline on test set with faithfulness, answer_relevancy, context_precision, context_recall
"""

import pandas as pd
import json
from ragas import evaluate
from ragas.metrics import (
    faithfulness, answer_relevancy,
    context_precision, context_recall
)
from datasets import Dataset
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Mock RAG pipeline function - replace with actual implementation
def mock_rag_pipeline(question):
    """
    Mock RAG pipeline for demonstration.
    In production, replace this with your actual RAG implementation from Day 18.
    """
    # Simple mock: return a relevant answer based on the question
    answers = {
        "decree": "Decree 13/2023/ND-CP is Vietnam's first comprehensive personal data protection law, effective July 1, 2023.",
        "principles": "The key principles include lawfulness, purpose limitation, data minimization, accuracy, storage limitation, and security.",
        "breach": "Data breaches must be reported to the Ministry of Public Security within 72 hours of discovery.",
        "consent": "Consent must be freely given, specific, informed, unambiguous, documented, and revocable.",
        "transfer": "Cross-border data transfer is generally prohibited unless specific conditions like adequate protection or explicit consent are met.",
        "dpo": "A Data Protection Officer must be appointed for large-scale processing, public authorities, or high-risk processing activities.",
    }
    
    # Simple keyword matching for demo
    for key, answer in answers.items():
        if key in question.lower():
            return answer, ["Vietnamese Personal Data Protection Decree (Decree 13/2023/ND-CP)"]
    
    return "This is a mock answer for demonstration purposes.", ["Vietnamese Personal Data Protection Decree (Decree 13/2023/ND-CP)"]

# Load test set
print("Loading test set...")
testset = pd.read_csv("testset_v1.csv")
print(f"Loaded {len(testset)} questions")

# Run RAG pipeline on each question
print("Running RAG pipeline on questions...")
results_data = []
for idx, row in testset.iterrows():
    question = row['question']
    ground_truth = row['ground_truth']
    contexts = eval(row['contexts']) if isinstance(row['contexts'], str) else row['contexts']
    
    # Run RAG pipeline
    answer, retrieved_contexts = mock_rag_pipeline(question)
    
    results_data.append({
        'question': question,
        'answer': answer,
        'contexts': retrieved_contexts,
        'ground_truth': ground_truth
    })
    
    if (idx + 1) % 10 == 0:
        print(f"Processed {idx + 1}/{len(testset)} questions")

# Create dataset
print("Creating dataset for evaluation...")
dataset = Dataset.from_list(results_data)

# Evaluate with RAGAS
print("Running RAGAS evaluation (this may take several minutes)...")
start_time = time.time()

scores = evaluate(
    dataset,
    metrics=[faithfulness, answer_relevancy, context_precision, context_recall],
    llm=ChatOpenAI(model="gpt-4o-mini")
)

elapsed_time = time.time() - start_time
print(f"Evaluation completed in {elapsed_time:.2f} seconds")

# Save results
print("Saving results...")
results_df = scores.to_pandas()
results_df.to_csv("ragas_results.csv", index=False)

# Save summary
summary = {
    'faithfulness': float(scores['faithfulness']),
    'answer_relevancy': float(scores['answer_relevancy']),
    'context_precision': float(scores['context_precision']),
    'context_recall': float(scores['context_recall']),
    'evaluation_time_seconds': elapsed_time,
    'total_questions': len(testset)
}

with open('ragas_summary.json', 'w') as f:
    json.dump(summary, f, indent=2)

print("\n=== RAGAS Evaluation Results ===")
print(f"Faithfulness: {summary['faithfulness']:.3f}")
print(f"Answer Relevancy: {summary['answer_relevancy']:.3f}")
print(f"Context Precision: {summary['context_precision']:.3f}")
print(f"Context Recall: {summary['context_recall']:.3f}")
print(f"\nResults saved to ragas_results.csv")
print(f"Summary saved to ragas_summary.json")

# Cost estimation (approximate)
estimated_cost = len(testset) * 0.002  # Rough estimate in USD
print(f"\nEstimated evaluation cost: ${estimated_cost:.2f}")
