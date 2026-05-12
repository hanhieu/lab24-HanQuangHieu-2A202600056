"""
Phase B.1 - Pairwise Judge Pipeline
Compare two versions of RAG answers with swap-and-average for position bias mitigation
"""

import json
import pandas as pd
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

JUDGE_PROMPT = PromptTemplate.from_template("""You are an impartial evaluator. Compare two answers to the same question.

Question: {question}
Answer A: {answer_a}
Answer B: {answer_b}

Rate based on:
- Factual accuracy
- Relevance to question
- Conciseness

Output JSON only:
{{"winner": "A" or "B" or "tie", "reason": "..."}}""")

def parse_judge_output(text):
    """Robust JSON parsing with fallback."""
    try:
        # Strip markdown code fences if any
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        return {"winner": "tie", "reason": "Parse error"}

def pairwise_judge_with_swap(question, ans1, ans2, judge_llm):
    """Swap-and-average for position bias mitigation."""
    results = []
    
    # Run 1: ans1 first, ans2 second
    prompt = JUDGE_PROMPT.format(question=question, answer_a=ans1, answer_b=ans2)
    out = judge_llm.invoke(prompt)
    r1 = parse_judge_output(out.content)
    results.append(r1)
    
    # Run 2: swap order
    prompt = JUDGE_PROMPT.format(question=question, answer_a=ans2, answer_b=ans1)
    out = judge_llm.invoke(prompt)
    r2 = parse_judge_output(out.content)
    # IMPORTANT: flip winner because order was swapped
    if r2['winner'] == 'A':
        r2['winner'] = 'B'
    elif r2['winner'] == 'B':
        r2['winner'] = 'A'
    results.append(r2)
    
    # Aggregate: both agree -> that. Disagree -> tie.
    if results[0]['winner'] == results[1]['winner']:
        return results[0]['winner'], results[0], results[1]
    return 'tie', results[0], results[1]

# Mock answers for comparison (simulating two RAG versions)
def generate_mock_answers():
    """Generate mock answers from two RAG versions for comparison."""
    testset = pd.read_csv("phase-a/testset_v1.csv").head(30)
    
    results = []
    for idx, row in testset.iterrows():
        question = row['question']
        
        # Version A: Basic RAG (shorter, simpler answers)
        answer_a = f"This is Version A answer for: {question[:50]}..."
        
        # Version B: Enhanced RAG with re-ranker (longer, more detailed)
        answer_b = f"This is Version B answer (enhanced with re-ranker) for: {question[:50]}... It provides more detailed information and context."
        
        results.append({
            'question': question,
            'answer_a': answer_a,
            'answer_b': answer_b
        })
    
    return pd.DataFrame(results)

# Main execution
if __name__ == "__main__":
    print("Setting up judge LLM...")
    judge_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    
    print("Generating mock answers from two RAG versions...")
    answers_df = generate_mock_answers()
    
    print("Running pairwise comparison with swap-and-average...")
    results = []
    for idx, row in answers_df.iterrows():
        question = row['question']
        ans1 = row['answer_a']
        ans2 = row['answer_b']
        
        winner, run1, run2 = pairwise_judge_with_swap(question, ans1, ans2, judge_llm)
        
        results.append({
            'question': question[:100],
            'answer_a': ans1[:50],
            'answer_b': ans2[:50],
            'run1_winner': run1['winner'],
            'run2_winner': run2['winner'],
            'winner_after_swap': winner,
            'run1_reason': run1.get('reason', ''),
            'run2_reason': run2.get('reason', '')
        })
        
        if (idx + 1) % 5 == 0:
            print(f"Processed {idx + 1}/{len(answers_df)} comparisons")
    
    # Save results
    results_df = pd.DataFrame(results)
    results_df.to_csv("phase-b/pairwise_results.csv", index=False)
    
    print(f"\n✓ Pairwise comparison complete!")
    print(f"Results saved to phase-b/pairwise_results.csv")
    
    # Print summary
    print("\n=== Summary ===")
    print(f"Total comparisons: {len(results_df)}")
    print(f"Winner distribution:")
    print(results_df['winner_after_swap'].value_counts())
