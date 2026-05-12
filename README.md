# Lab 24: RAG Evaluation and Guardrail System

A comprehensive evaluation and guardrail system for a Retrieval-Augmented Generation (RAG) pipeline, implementing RAGAS metrics, LLM-as-Judge evaluation, and input/output guardrails for production deployment.

## Project Structure

```
lab24-HanQuangHieu-2A202600056/
├── docs/                      # Corpus documents (Vietnamese data protection)
│   ├── doc1.md              # Personal Data Protection Decree overview
│   ├── doc2.md              # Data Breach Notification Requirements
│   ├── doc3.md              # Cross-Border Data Transfer Regulations
│   ├── doc4.md              # Data Processing Consent Requirements
│   └── doc5.md              # DPO Requirements
├── phase-a/                   # Phase A: RAGAS Evaluation
│   ├── generate_testset.py   # Synthetic test set generation
│   ├── run_ragas_eval.py    # RAGAS evaluation pipeline
│   ├── testset_v1.csv       # Generated test set (50 questions)
│   ├── testset_review_notes.md # Manual review documentation
│   ├── ragas_results.csv     # Detailed RAGAS scores
│   ├── ragas_summary.json   # Summary metrics and observations
│   └── failure_analysis.md  # Failure cluster analysis
├── phase-b/                   # Phase B: LLM-as-Judge & Calibration
│   ├── pairwise_judge.py    # Pairwise comparison with swap-and-average
│   ├── pairwise_results.csv  # Mock pairwise comparison results
│   ├── absolute_scoring.py   # Absolute scoring with 4-point rubric
│   ├── absolute_scores.csv   # Mock absolute scoring results
│   ├── kappa_analysis.py     # Human calibration with Cohen's Kappa
│   ├── human_labels.csv      # Mock human labels for calibration
│   └── judge_bias_report.md  # Judge bias analysis
├── phase-c/                   # Phase C: Guardrails Stack
│   ├── input_guard.py        # PII redaction with Presidio
│   ├── pii_test_results.csv  # PII detection test results
│   ├── output_guard.py       # Toxicity detection with LLM-as-Judge
│   ├── toxicity_test_results.csv # Toxicity detection test results
│   ├── guardrail_pipeline.py # Full guardrail integration
│   └── pipeline_test_results.csv # End-to-end pipeline test results
├── .github/workflows/         # CI/CD integration
│   └── eval-gate.yml        # GitHub Actions evaluation gate
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variables template
└── README.md                  # This file
```

## Phase A: RAGAS Evaluation

### A.1: Synthetic Test Set Generation
- **File**: `phase-a/generate_testset.py`
- **Output**: `phase-a/testset_v1.csv` (50 questions)
- **Distribution**: 50% simple, 25% reasoning, 25% multi-context
- **Review**: `phase-a/testset_review_notes.md`

### A.2: RAGAS Evaluation
- **File**: `phase-a/run_ragas_eval.py`
- **Metrics**: Faithfulness, Answer Relevancy, Context Precision, Context Recall
- **Output**: `phase-a/ragas_results.csv`, `phase-a/ragas_summary.json`

### A.3: Failure Cluster Analysis
- **File**: `phase-a/failure_analysis.md`
- **Analysis**: Bottom 10 questions, failure patterns, root causes, fixes

### A.4: CI/CD Integration
- **File**: `.github/workflows/eval-gate.yml`
- **Function**: GitHub Actions workflow to gate PR merges on evaluation thresholds

## Phase B: LLM-as-Judge & Calibration

### B.1: Pairwise Comparison
- **File**: `phase-b/pairwise_judge.py`
- **Feature**: Swap-and-average to mitigate position bias
- **Output**: `phase-b/pairwise_results.csv`

### B.2: Absolute Scoring
- **File**: `phase-b/absolute_scoring.py`
- **Rubric**: 4 dimensions (accuracy, relevance, conciseness, helpfulness) on 1-5 scale
- **Output**: `phase-b/absolute_scores.csv`

### B.3: Human Calibration
- **File**: `phase-b/kappa_analysis.py`
- **Metric**: Cohen's Kappa for agreement measurement
- **Output**: Mock human labels in `phase-b/human_labels.csv`

### B.4: Judge Bias Analysis
- **File**: `phase-b/judge_bias_report.md`
- **Analysis**: Position bias, length bias, style bias with mitigation strategies

## Phase C: Guardrails Stack

### C.1: Input Guardrail - PII Redaction
- **File**: `phase-c/input_guard.py`
- **Technology**: Presidio + Vietnamese regex patterns
- **Features**: 
  - VN-specific PII detection (CCCD, phone, tax code, email)
  - Presidio NER for multilingual support
  - Latency tracking (<50ms P95 target)
- **Output**: `phase-c/pii_test_results.csv`

### C.2: Output Guardrail - Toxicity Detection
- **File**: `phase-c/output_guard.py`
- **Technology**: LLM-as-Judge (GPT-4o-mini)
- **Features**:
  - Binary toxicity classification
  - JSON response format
  - Latency tracking (<100ms P95 target)
- **Output**: `phase-c/toxicity_test_results.csv`

### C.3: Full Pipeline Integration
- **File**: `phase-c/guardrail_pipeline.py`
- **Features**:
  - End-to-end guardrail orchestration
  - Input sanitization + output validation
  - Comprehensive metadata tracking
  - Latency benchmarking (<200ms P95 target)
- **Output**: `phase-c/pipeline_test_results.csv`

## Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your API keys
```

## Usage

### Run RAGAS Evaluation
```bash
cd phase-a
python generate_testset.py
python run_ragas_eval.py
```

### Run LLM-as-Judge Evaluation
```bash
cd phase-b
python pairwise_judge.py
python absolute_scoring.py
python kappa_analysis.py
```

### Run Guardrail Tests
```bash
cd phase-c
python input_guard.py
python output_guard.py
python guardrail_pipeline.py
```

## Results Summary

### RAGAS Metrics
- **Faithfulness**: 0.82
- **Answer Relevancy**: 0.78
- **Context Precision**: 0.85
- **Context Recall**: 0.75

### Guardrail Performance
- **PII Detection Rate**: 80%+
- **PII P95 Latency**: <50ms
- **Toxicity Detection**: Functional
- **Toxicity P95 Latency**: <100ms
- **End-to-End P95 Latency**: <200ms

### Judge Calibration
- **Cohen's Kappa**: Demonstrated calculation
- **Bias Mitigation**: Swap-and-average implemented

## Requirements

- Python 3.10+
- OpenAI API key (for LLM-as-Judge)
- Dependencies listed in `requirements.txt`

## Key Technologies

- **RAGAS**: RAG evaluation metrics
- **Presidio**: PII detection and redaction
- **OpenAI API**: LLM-as-Judge implementation
- **LangChain**: RAG pipeline framework
- **Pandas**: Data processing
- **scikit-learn**: Kappa calculation

## Notes

- All test results are mock/simulated for demonstration purposes
- Replace mock data with actual RAG pipeline outputs for production use
- Adjust evaluation thresholds in `.github/workflows/eval-gate.yml` as needed
- Vietnamese-specific PII patterns can be extended in `phase-c/input_guard.py`

## License

This project is part of Lab 24 requirements fulfillment.
 educational purposes.
