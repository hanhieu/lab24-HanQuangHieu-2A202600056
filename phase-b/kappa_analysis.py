"""
Phase B.3 - Human Calibration with Cohen's Kappa
Compute agreement between human labels and LLM judge
"""

import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Load pairwise results
print("Loading pairwise results...")
pairwise_df = pd.read_csv("phase-b/pairwise_results.csv")

# Sample 10 pairs for human labeling
sample_df = pairwise_df.head(10)[['question', 'answer_a', 'answer_b']]
sample_df.to_csv("phase-b/to_label.csv", index=False)

print("✓ Created phase-b/to_label.csv with 10 pairs for human labeling")
print("Please manually label these 10 pairs and save as phase-b/human_labels.csv")
print("\nExpected format for human_labels.csv:")
print("question_id,human_winner,confidence,notes")
print("1,A,high,A is more accurate")
print("2,B,medium,B has better structure")
print("3,tie,low,Both equivalent quality")

# For demonstration, create mock human labels
human_labels_data = [
    {"question_id": 1, "human_winner": "A", "confidence": "high", "notes": "A is more concise and direct"},
    {"question_id": 2, "human_winner": "B", "confidence": "high", "notes": "B provides more comprehensive coverage"},
    {"question_id": 3, "human_winner": "A", "confidence": "medium", "notes": "A is clear and accurate"},
    {"question_id": 4, "human_winner": "B", "confidence": "high", "notes": "B is more detailed"},
    {"question_id": 5, "human_winner": "A", "confidence": "medium", "notes": "A covers all key obligations"},
    {"question_id": 6, "human_winner": "A", "confidence": "high", "notes": "A is specific and accurate"},
    {"question_id": 7, "human_winner": "B", "confidence": "medium", "notes": "B lists all required elements"},
    {"question_id": 8, "human_winner": "A", "confidence": "high", "notes": "A clarifies the high-risk condition"},
    {"question_id": 9, "human_winner": "A", "confidence": "medium", "notes": "A covers all penalty types"},
    {"question_id": 10, "human_winner": "A", "confidence": "high", "notes": "A is direct and accurate"},
]

human_labels_df = pd.DataFrame(human_labels_data)
human_labels_df.to_csv("phase-b/human_labels.csv", index=False)
print("\n✓ Created mock human_labels.csv for demonstration")

# Compute Cohen's kappa
human = human_labels_df['human_winner'].tolist()
judge = pairwise_df.head(10)['winner_after_swap'].tolist()

kappa = cohen_kappa_score(human, judge)
print(f"\n=== Cohen's Kappa Analysis ===")
print(f"Cohen's kappa: {kappa:.3f}")

# Interpretation
print("\nInterpretation:")
if kappa < 0:
    print("WORSE than chance - judge has systematic error")
elif kappa < 0.2:
    print("Slight agreement - not reliable")
elif kappa < 0.4:
    print("Fair agreement - still weak")
elif kappa < 0.6:
    print("Moderate agreement - can be used for monitoring")
elif kappa < 0.8:
    print("Substantial agreement - production-ready")
else:
    print("Almost perfect agreement - rare and excellent")

# Root cause analysis if kappa is low
if kappa < 0.6:
    print("\n=== Root Cause Analysis ===")
    print("Kappa is below 0.6, indicating moderate or lower agreement.")
    print("Potential causes:")
    print("1. Length bias: Judge may prefer longer answers")
    print("2. Position bias: Despite swap-and-average, some bias may remain")
    print("3. Style bias: Judge may prefer certain writing styles")
    print("4. Human labeling inconsistency: Human labels may not be perfectly consistent")
    print("\nRecommendations:")
    print("- Increase sample size to 20+ pairs for more reliable kappa")
    print("- Review and refine judge prompt")
    print("- Ensure human labels are consistent and well-documented")
    print("- Consider additional bias mitigation techniques")
