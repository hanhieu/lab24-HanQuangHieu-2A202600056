# Phase D.2: Architecture Diagram

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE LAYER                              │
└──────────────────────────────┬──────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        API GATEWAY / LOAD BALANCER                         │
│                    (Rate Limiting, Auth, Request Routing)                      │
└──────────────────────────────┬──────────────────────────────────────────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  INPUT GUARD  │    │   RAG PIPELINE  │    │ OUTPUT GUARD  │
│               │    │               │    │               │
│  - PII Detect │    │  - Retrieval   │    │  - Toxicity   │
│  - Redaction   │───▶│  - Generation  │───▶│  - Blocking    │
│  - Latency    │    │  - Context    │    │  - Logging    │
└───────────────┘    └───────┬───────┘    └───────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│  QDRANT       │    │  LLM SERVICE  │    │  MONITORING   │
│  VECTOR DB    │    │  (OpenAI/     │    │  & ALERTING   │
│               │    │   Anthropic)   │    │               │
│  - Embeddings │    │               │    │  - Metrics    │
│  - Similarity │    │  - Inference  │    │  - Dashboards │
│  - Storage    │    │  - Caching    │    │  - SLO Track  │
└───────────────┘    └───────────────┘    └───────────────┘
        │                     │                     │
        └─────────────────────┴─────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        EVALUATION LAYER                                   │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   RAGAS      │  │  LLM-as-Judge│  │  CALIBRATION │          │
│  │   Metrics    │  │  (Pairwise/  │  │  (Kappa)     │          │
│  │   (4 metrics)│  │   Absolute)   │  │              │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │   FAILURE    │  │   BIAS       │  │   CI/CD      │          │
│  │   ANALYSIS   │  │   ANALYSIS    │  │   GATE       │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
└─────────────────────────────────────────────────────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                        DATA & STORAGE LAYER                               │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │  CORPUS     │  │  TEST SET    │  │  RESULTS     │          │
│  │  (Markdown)  │  │  (CSV/JSON)  │  │  (CSV/JSON)  │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
│                                                                      │
│  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐          │
│  │  HUMAN      │  │  GUARDRAIL   │  │  EVALUATION  │          │
│  │  LABELS     │  │  LOGS       │  │  LOGS       │          │
│  └───────────────┘  └───────────────┘  └───────────────┘          │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Input Guardrail Layer
- **Technology**: Presidio + Custom Regex
- **Function**: PII detection and redaction
- **Latency**: <50ms P95
- **Coverage**: VN-specific patterns (CCCD, phone, tax code)

### 2. RAG Pipeline
- **Retrieval**: Qdrant vector database
- **Generation**: LLM service (OpenAI/Anthropic)
- **Context**: Vietnamese data protection corpus
- **Latency**: <300ms P95

### 3. Output Guardrail Layer
- **Technology**: LLM-as-Judge (GPT-4o-mini)
- **Function**: Toxicity detection
- **Latency**: <100ms P95
- **Action**: Block toxic responses

### 4. Evaluation Layer
- **RAGAS**: Faithfulness, relevancy, context precision/recall
- **LLM-as-Judge**: Pairwise + absolute scoring
- **Calibration**: Cohen's Kappa for human agreement
- **Bias Analysis**: Position, length, style bias mitigation

### 5. CI/CD Integration
- **Platform**: GitHub Actions
- **Trigger**: Pull requests
- **Gate**: Evaluation threshold checks
- **Action**: Block merges on failure

### 6. Monitoring & Alerting
- **Metrics**: Latency, accuracy, availability
- **Dashboards**: Real-time visualization
- **Alerts**: SLO breach notifications
- **SLO Tracking**: Monthly compliance reports

## Data Flow

1. **User Query** → Input Guardrail (PII redaction)
2. **Sanitized Query** → RAG Pipeline (retrieval + generation)
3. **RAG Response** → Output Guardrail (toxicity check)
4. **Safe Response** → User
5. **Evaluation Jobs** → Run periodically/on-demand
6. **Results** → Stored for analysis and CI/CD gating

## Technology Stack

- **Vector Database**: Qdrant
- **LLM**: OpenAI GPT-4 / Anthropic Claude
- **Evaluation**: RAGAS, custom LLM-as-Judge
- **Guardrails**: Presidio, OpenAI API
- **CI/CD**: GitHub Actions
- **Monitoring**: Custom metrics + alerting
- **Storage**: Local file system (CSV/JSON/Markdown)
