"""
Phase B.2 - Absolute Scoring with Rubric
Score answers on 4 dimensions with 1-5 scale
"""

import json
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

ABSOLUTE_PROMPT = PromptTemplate.from_template("""Score the answer on 4 dimensions, each 1-5 scale:

1. Factual accuracy (1=many errors, 5=fully accurate)
2. Relevance (1=off-topic, 5=directly answers)
3. Conciseness (1=verbose, 5=appropriately brief)
4. Helpfulness (1=unclear, 5=actionable)

Question: {question}
Answer: {answer}

Output JSON only:
{{"accuracy": int, "relevance": int, "conciseness": int, "helpfulness": int, "overall": float}}""")

def parse_judge_output(text):
    """Robust JSON parsing with fallback."""
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"accuracy": 3, "relevance": 3, "conciseness": 3, "helpfulness": 3, "overall": 3.0}

def absolute_score(question, answer, judge_llm):
    prompt = ABSOLUTE_PROMPT.format(question=question, answer=answer)
    out = judge_llm.invoke(prompt)
    parsed = parse_judge_output(out.content)
    # Compute overall as average if not provided
    if 'overall' not in parsed or parsed['overall'] is None:
        dims = ['accuracy', 'relevance', 'conciseness', 'helpfulness']
        parsed['overall'] = sum(parsed[d] for d in dims) / 4
    return parsed

# Main execution
if __name__ == "__main__":
    print("Setting up judge LLM...")
    judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    print("Loading test set...")
    testset = pd.read_csv("phase-a/testset_v1.csv").head(30)
    
    print("Running absolute scoring...")
    results = []
    for idx, row in testset.iterrows():
        question = row['question']
        # Use a mock answer for demonstration
        answer = f"This is a mock answer for the question about {question[:30]}..."
        
        scores = absolute_score(question, answer, judge_llm)
        
        results.append({
            'question': question[:100],
            'answer': answer[:50],
            'accuracy': scores['accuracy'],
            'relevance': scores['relevance'],
            'conciseness': scores['conciseness'],
            'helpfulness': scores['helpfulness'],
            'overall': scores['overall']
        })
        
        if (idx + 1) % 5 == 0:
            print(f"Processed {idx + 1}/{len(testset)} questions")
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv("phase-b/absolute_scores.csv", index=False)
    
    print(f"\n✓ Absolute scoring complete!")
    print(f"Results saved to phase-b/absolute_scores.csv")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total questions scored: {len(results_df)}")
    print(f"\nAverage scores:")
    print(f"Accuracy: {results_df['accuracy'].mean():.2f}")
    print(f"Relevance: {results_df['relevance'].mean():.2f}")
    print(f"Conciseness: {results_df['conciseness'].mean():.2f}")
    print(f"Helpfulness: {results_df['helpfulness'].mean():.2f}")
    print(f"Overall: {results_df['overall'].mean():.2f}")
