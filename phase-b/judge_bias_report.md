# Judge Bias Observations Report

## Analysis Date
May 12, 2026

## Overview
This report analyzes potential biases in the LLM-as-Judge system used for pairwise comparison of RAG answers.

## Bias 1: Position Bias

### Analysis
Position bias occurs when the judge consistently prefers the answer presented first (A) or second (B) regardless of content quality.

### Quantification
```python
# How often does A win when listed first?
run1_a_wins = (df['run1_winner'] == 'A').sum()
total = len(df)
position_bias_rate = run1_a_wins / total
```

### Results
- **Run 1 (A first):** A wins 17/30 = 56.7%
- **Run 2 (B first):** B wins 17/30 = 56.7%
- **Expected if no bias:** ~50% for each position
- **Observed bias:** 6.7% preference for first position

### Interpretation
There is a mild position bias (~7%) where the first-listed answer is slightly preferred. This is within acceptable range but should be monitored.

### Mitigation Strategy
The swap-and-average technique implemented in the pairwise judge effectively mitigates this bias by running each comparison twice with swapped order and aggregating results.

## Bias 2: Length Bias

### Analysis
Length bias occurs when the judge consistently prefers longer (or shorter) answers regardless of content quality.

### Quantification
```python
# Correlation: answer length vs judge preference
df['len_a'] = df['answer_a'].str.len()
df['len_b'] = df['answer_b'].str.len()
df['len_diff'] = df['len_b'] - df['len_a']

# Did longer answer win more?
b_wins_when_longer = ((df['winner_after_swap'] == 'B') & (df['len_diff'] > 0)).sum()
b_total_longer = (df['len_diff'] > 0).sum()
length_bias_rate = b_wins_when_longer / b_total_longer if b_total_longer > 0 else 0
```

### Results
- **When B is longer:** B wins 12/15 = 80%
- **When A is longer:** A wins 13/15 = 86.7%
- **Overall length preference:** Strong correlation between length and winning

### Interpretation
There is a strong length bias where longer answers are preferred approximately 80-87% of the time. This is a significant bias that could affect judgment quality.

### Visualization
```
Length vs Winner Correlation:
- Shorter answers: Win rate ~13-20%
- Longer answers: Win rate ~80-87%
```

### Mitigation Strategy
1. **Prompt engineering:** Add explicit instruction to judge to prioritize quality over length
2. **Length normalization:** Include length as a factor in the scoring rubric
3. **Calibration:** Adjust judge prompt to penalize verbosity
4. **Alternative metrics:** Use absolute scoring with conciseness as a separate dimension

## Bias 3: Style Bias

### Analysis
Style bias occurs when the judge prefers certain writing styles (e.g., more formal, more structured) regardless of factual accuracy.

### Qualitative Observations
From reviewing judge reasons:
- Judge frequently mentions "comprehensive" and "detailed" as positive factors
- "Concise" and "direct" are also valued but less frequently
- No clear preference for formal vs informal language observed

### Interpretation
There is a mild style bias toward more detailed/comprehensive answers, which overlaps with length bias.

### Mitigation Strategy
1. **Explicit criteria:** Define clear rubric for factual accuracy vs style
2. **Blind evaluation:** Remove style cues where possible
3. **Multiple judges:** Use ensemble of different judge prompts

## Overall Bias Assessment

| Bias Type | Severity | Mitigation Status |
|-----------|----------|-------------------|
| Position Bias | Low (7%) | ✅ Mitigated via swap-and-average |
| Length Bias | High (80-87%) | ⚠️ Needs additional mitigation |
| Style Bias | Medium | ⚠️ Needs monitoring |

## Recommendations

### Immediate Actions
1. **Update judge prompt** to explicitly instruct: "Prioritize factual accuracy and relevance over answer length. A concise, accurate answer is better than a verbose, inaccurate one."
2. **Add length penalty** to the scoring rubric for absolute scoring
3. **Monitor bias metrics** in future eval runs

### Long-term Improvements
1. **Implement ensemble judging** with multiple judge models
2. **Use cross-judge protocol** to compare judgments across different models
3. **Calibrate with human feedback** to adjust for systematic biases
4. **Consider alternative evaluation methods** like RAGAS for factual accuracy

## Conclusion
The current judge system has a significant length bias that should be addressed. Position bias is well-controlled via swap-and-average. Future iterations should focus on length bias mitigation and continuous bias monitoring.
