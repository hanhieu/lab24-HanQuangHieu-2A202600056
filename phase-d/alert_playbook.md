# Phase D.3: Alert Playbook

## Overview
This playbook defines alert conditions, severity levels, and response procedures for the RAG evaluation and guardrail system.

## Alert Conditions

### 1. Latency Alerts

#### P50 Latency Breach
- **Condition**: P50 latency > 250ms for 5 consecutive minutes
- **Severity**: Warning
- **Component**: End-to-end query processing

#### P95 Latency Breach
- **Condition**: P95 latency > 500ms for 5 consecutive minutes
- **Severity**: Critical
- **Component**: End-to-end query processing

#### Component-Specific Latency
- **Input Guardrail**: P95 > 50ms (Warning), > 100ms (Critical)
- **RAG Pipeline**: P95 > 300ms (Warning), > 500ms (Critical)
- **Output Guardrail**: P95 > 100ms (Warning), > 200ms (Critical)

### 2. Quality Alerts

#### RAGAS Metric Breach
- **Condition**: Any metric below target for 3 consecutive evaluations
- **Severity**: Warning
- **Metrics**: Faithfulness < 0.80, Relevancy < 0.75, Context Precision < 0.80, Context Recall < 0.75

#### Guardrail Detection Rate Drop
- **Condition**: Detection rate drops 10% from baseline for 1 hour
- **Severity**: Warning
- **Components**: PII detection, Toxicity detection

#### False Positive Spike
- **Condition**: False positive rate > 10% for 30 minutes
- **Severity**: Warning
- **Impact**: User experience degradation

### 3. Availability Alerts

#### API Endpoint Down
- **Condition**: Health check fails for 2 consecutive checks (1-minute interval)
- **Severity**: Critical
- **Component**: API Gateway

#### Evaluation Job Failure
- **Condition**: Evaluation job fails 3 times in a row
- **Severity**: Warning
- **Component**: Evaluation pipeline

#### System Uptime Breach
- **Condition**: Uptime < 99.5% for 1 hour
- **Severity**: Critical
- **Component**: Overall system

## Severity Levels

### Information (Info)
- **Color**: Blue
- **Action**: Log only, no immediate action required
- **Example**: Scheduled maintenance, metric trends

### Warning
- **Color**: Yellow
- **Action**: Investigate within 1 hour, resolve within 4 hours
- **Escalation**: Notify team lead if not resolved in 2 hours

### Critical
- **Color**: Red
- **Action**: Investigate immediately, resolve within 1 hour
- **Escalation**: Notify on-call engineer immediately, team lead in 30 minutes

## Response Procedures

### Latency Breach (Critical)

1. **Immediate (0-5 minutes)**
   - Check system load and resource utilization
   - Verify all components are healthy
   - Check for network issues or external API delays

2. **Investigation (5-30 minutes)**
   - Review recent deployments or configuration changes
   - Check database query performance
   - Analyze component-specific latency breakdown

3. **Resolution (30-60 minutes)**
   - Scale resources if needed
   - Optimize slow queries
   - Cache frequently accessed data
   - Roll back recent changes if necessary

4. **Post-Incident**
   - Document root cause
   - Update runbooks if needed
   - Review SLO compliance impact

### Quality Metric Breach (Warning)

1. **Immediate (0-30 minutes)**
   - Review recent evaluation results
   - Check for data quality issues
   - Verify evaluation pipeline integrity

2. **Investigation (30-120 minutes)**
   - Analyze failure patterns
   - Review corpus changes
   - Check model drift

3. **Resolution (2-4 hours)**
   - Retrain or fine-tune models
   - Update corpus with better examples
   - Adjust evaluation thresholds if appropriate

### Availability Breach (Critical)

1. **Immediate (0-5 minutes)**
   - Check service health endpoints
   - Verify infrastructure status
   - Check for DDoS or traffic spikes

2. **Investigation (5-30 minutes)**
   - Review error logs
   - Check dependency services (OpenAI, Qdrant)
   - Verify auto-scaling triggers

3. **Resolution (30-60 minutes)**
   - Restart failed services
   - Scale up infrastructure
   - Failover to backup if needed
   - Implement rate limiting if under attack

### Guardrail Failure (Warning)

1. **Immediate (0-30 minutes)**
   - Review guardrail logs
   - Check for pattern changes
   - Verify regex rules and model prompts

2. **Investigation (30-120 minutes)**
   - Test guardrail on known samples
   - Check for model degradation
   - Review false positive examples

3. **Resolution (2-4 hours)**
   - Update regex patterns
   - Adjust model prompts
   - Add new training examples
   - Tune detection thresholds

## Escalation Matrix

| Severity | Time to Resolve | Escalation To |
|----------|-----------------|----------------|
| Warning  | 4 hours         | Team Lead       |
| Critical | 1 hour          | On-call Engineer + Team Lead |
| Critical (unresolved) | 2 hours  | Engineering Manager |

## On-Call Responsibilities

### Primary On-Call
- Monitor alerts 24/7
- Acknowledge alerts within 15 minutes
- Begin investigation within 30 minutes
- Document all actions

### Backup On-Call
- Available if primary is unavailable
- Same response time requirements
- Handoff procedure documented

## Communication

### During Incident
- **Internal**: Slack channel #incidents
- **Stakeholders**: Email updates every 30 minutes for critical incidents
- **Public**: Status page updates for outages > 30 minutes

### Post-Incident
- **RCA**: Root Cause Analysis within 24 hours
- **Post-mortem**: Team review within 48 hours
- **Improvements**: Action items tracked and assigned

## Testing

### Alert Validation
- Monthly alert drill
- Test each alert condition
- Verify notification delivery
- Practice response procedures

### Playbook Maintenance
- Quarterly review of all procedures
- Update based on incident learnings
- Add new alert conditions as system evolves
