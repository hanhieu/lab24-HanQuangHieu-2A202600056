"""
Phase C.2 - Input Guardrail: Topic Scope Validator
Implement topic validator using embedding similarity (Option 1 - Basic)
"""

import numpy as np
from langchain_openai import OpenAIEmbeddings
import os

class TopicGuard:
    def __init__(self, allowed_topics: list[str]):
        self.embeddings = OpenAIEmbeddings(api_key=os.getenv("OPENAI_API_KEY"))
        self.topic_vectors = [self.embeddings.embed_query(t) for t in allowed_topics]
        self.topics = allowed_topics

    def check(self, text: str) -> tuple[bool, str]:
        """
        Check if text is within allowed topics using embedding similarity.
        Returns (is_allowed, reason)
        """
        q_vec = self.embeddings.embed_query(text)
        sims = [
            np.dot(q_vec, tv) / (np.linalg.norm(q_vec) * np.linalg.norm(tv))
            for tv in self.topic_vectors
        ]
        max_sim = max(sims)
        best_topic = self.topics[sims.index(max_sim)]
        
        if max_sim > 0.6:
            return True, f"On topic: {best_topic}"
        return False, f"Off topic. Closest: {best_topic} ({max_sim:.2f})"

# Define allowed topics for Vietnamese data protection domain
ALLOWED_TOPICS = [
    "Vietnamese personal data protection law",
    "Data breach notification requirements",
    "Cross-border data transfer regulations",
    "Data processing consent requirements",
    "Data Protection Officer responsibilities",
    "Data subject rights under Decree 13",
    "Data controller obligations",
    "Sensitive data categories",
    "Data retention policies",
    "Compliance and penalties"
]

# Test set: 20 inputs (10 on-topic, 10 off-topic)
test_inputs = [
    # On-topic (10)
    "What are the requirements for data breach notification under Decree 13?",
    "How do I transfer personal data across borders legally?",
    "What rights do data subjects have under Vietnamese law?",
    "When is consent required for data processing?",
    "What are the responsibilities of a Data Protection Officer?",
    "What constitutes sensitive personal data in Vietnam?",
    "What are the penalties for non-compliance with data protection laws?",
    "How long can personal data be retained?",
    "What is the process for appointing a DPO?",
    "What are the obligations of data controllers?",
    
    # Off-topic (10)
    "How do I bake a chocolate cake?",
    "What is the capital of France?",
    "How do I fix a leaking faucet?",
    "What are the best programming languages for web development?",
    "How do I invest in stocks?",
    "What is the weather like today?",
    "How do I train a dog to sit?",
    "What are the health benefits of yoga?",
    "How do I write a resume?",
    "What is the meaning of life?"
]

if __name__ == "__main__":
    print("Initializing Topic Guard...")
    guard = TopicGuard(ALLOWED_TOPICS)
    
    print("Running topic validation tests...")
    results = []
    for idx, test_input in enumerate(test_inputs):
        is_allowed, reason = guard.check(test_input)
        
        # Determine expected (first 10 are on-topic, last 10 are off-topic)
        expected = idx < 10
        correct = is_allowed == expected
        
        results.append({
            'input': test_input[:50],
            'is_allowed': is_allowed,
            'reason': reason,
            'expected': expected,
            'correct': correct
        })
        
        status = "✓" if correct else "✗"
        print(f"[{idx+1}/20] {status} Allowed: {is_allowed}, Reason: {reason}")
    
    # Save results
    import pandas as pd
    results_df = pd.DataFrame(results)
    results_df.to_csv("phase-c/topic_test_results.csv", index=False)
    
    print(f"\n✓ Topic validation testing complete!")
    print(f"Results saved to phase-c/topic_test_results.csv")
    
    # Calculate metrics
    accuracy = results_df['correct'].sum() / len(results_df)
    on_topic_correct = results_df[results_df['expected'] == True]['correct'].sum() / 10
    off_topic_correct = results_df[results_df['expected'] == False]['correct'].sum() / 10
    refuse_rate = (~results_df['is_allowed']).sum() / len(results_df)
    
    print(f"\n=== Metrics ===")
    print(f"Overall accuracy: {accuracy:.1%}")
    print(f"On-topic accuracy: {on_topic_correct:.1%}")
    print(f"Off-topic accuracy: {off_topic_correct:.1%}")
    print(f"Refuse rate: {refuse_rate:.1%}")
    
    if accuracy >= 0.75:
        print("✓ Accuracy meets target (≥75%)")
    else:
        print("✗ Accuracy below target (≥75%)")
