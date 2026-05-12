"""
Phase C.5 - Full Stack Integration & Latency Benchmark
Integrate all guardrails with async/parallel execution and latency benchmarking
"""

import asyncio
import time
from typing import Dict, Tuple
from input_guard import InputGuard
from output_guard import OutputGuard
from topic_guard import TopicGuard

class GuardrailPipeline:
    def __init__(self):
        self.input_guard = InputGuard()
        self.output_guard = OutputGuard()
        self.topic_guard = TopicGuard([
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
        ])
        
    async def process_query_async(self, query: str) -> Tuple[str, Dict]:
        """
        Process user query through input guardrails (L1 parallel).
        Returns (sanitized_query, metadata)
        """
        start = time.perf_counter()
        
        # L1 parallel: PII redaction + Topic check
        pii_task = asyncio.create_task(asyncio.to_thread(self.input_guard.sanitize, query))
        topic_task = asyncio.create_task(asyncio.to_thread(self.topic_guard.check, query))
        
        sanitized_query, pii_found, input_latency = await pii_task
        topic_ok, topic_reason = await topic_task
        
        total_latency = (time.perf_counter() - start) * 1000
        
        metadata = {
            "original_query": query,
            "sanitized_query": sanitized_query,
            "pii_detected": len(pii_found) > 0,
            "pii_types": pii_found,
            "topic_ok": topic_ok,
            "topic_reason": topic_reason,
            "input_guard_latency_ms": round(input_latency, 2),
            "total_l1_latency_ms": round(total_latency, 2)
        }
        
        return sanitized_query, metadata
    
    async def process_response_async(self, user_input: str, response: str) -> Tuple[str, Dict]:
        """
        Process RAG response through output guardrail (L3).
        Returns (safe_response, metadata)
        """
        start = time.perf_counter()
        
        # L3: Llama Guard 3 check
        guard_result = await asyncio.to_thread(self.output_guard.check, user_input, response)
        
        total_latency = (time.perf_counter() - start) * 1000
        
        if not guard_result["is_safe"]:
            safe_response = "[RESPONSE BLOCKED: Unsafe content detected]"
        else:
            safe_response = response
        
        metadata = {
            "original_response": response,
            "safe_response": safe_response,
            "is_safe": guard_result["is_safe"],
            "guard_result": guard_result["result"],
            "output_guard_latency_ms": round(guard_result["latency_ms"], 2),
            "total_l3_latency_ms": round(total_latency, 2)
        }
        
        return safe_response, metadata
    
    async def full_pipeline_async(self, query: str, response: str) -> Dict:
        """
        Run full guardrail pipeline with end-to-end latency tracking.
        Architecture:
        L1 (parallel): PII + Topic
        L2: RAG pipeline (mock for this lab)
        L3: Llama Guard 3
        L4: Audit log (async, fire-and-forget)
        """
        timings = {}
        start = time.perf_counter()
        
        # L1: Input guards (parallel)
        t0 = time.perf_counter()
        sanitized_query, input_meta = await self.process_query_async(query)
        timings['L1'] = (time.perf_counter() - t0) * 1000
        
        if not input_meta['topic_ok']:
            return {
                "query": query,
                "sanitized_query": sanitized_query,
                "response": "[REFUSED: Off-topic query]",
                "safe_response": "[REFUSED: Off-topic query]",
                "timings": timings,
                "guardrails_triggered": {"topic": True, "pii": input_meta['pii_detected'], "output": False},
                "total_latency_ms": round((time.perf_counter() - start) * 1000, 2)
            }
        
        # L2: RAG pipeline (mock - in production this would be actual RAG)
        t0 = time.perf_counter()
        # Mock RAG latency: 200ms average
        await asyncio.sleep(0.2)
        timings['L2'] = (time.perf_counter() - t0) * 1000
        
        # L3: Output guard (Llama Guard 3)
        t0 = time.perf_counter()
        safe_response, output_meta = await self.process_response_async(sanitized_query, response)
        timings['L3'] = (time.perf_counter() - t0) * 1000
        
        if not output_meta['is_safe']:
            return {
                "query": query,
                "sanitized_query": sanitized_query,
                "response": response,
                "safe_response": safe_response,
                "timings": timings,
                "guardrails_triggered": {"topic": False, "pii": input_meta['pii_detected'], "output": True},
                "total_latency_ms": round((time.perf_counter() - start) * 1000, 2)
            }
        
        # L4: Audit log (async, fire-and-forget - doesn't count in latency budget)
        asyncio.create_task(self._audit_log(query, safe_response, timings))
        
        total_latency = (time.perf_counter() - start) * 1000
        
        return {
            "query": query,
            "sanitized_query": sanitized_query,
            "response": response,
            "safe_response": safe_response,
            "timings": timings,
            "guardrails_triggered": {"topic": False, "pii": input_meta['pii_detected'], "output": False},
            "total_latency_ms": round(total_latency, 2)
        }
    
    async def _audit_log(self, query: str, response: str, timings: Dict):
        """Async audit log (fire-and-forget, doesn't block pipeline)."""
        # In production, this would log to a database or logging service
        await asyncio.sleep(0.001)  # Simulate async write

# Test scenarios
test_scenarios = [
    {
        "query": "What is John Smith's email?",
        "response": "John Smith's email is john@example.com."
    },
    {
        "query": "Explain data breach notification requirements.",
        "response": "Under Decree 13/2023/ND-CP, data controllers must notify the Ministry of Public Security within 72 hours of discovering a breach."
    },
    {
        "query": "My CCCD is 012345678901, what are my rights?",
        "response": "You have the right to access, correct, and delete your personal data."
    },
    {
        "query": "What are the DPO requirements?",
        "response": "A DPO is required for organizations processing sensitive data on a large scale. They must be independent and qualified."
    },
    {
        "query": "How do I bake a cake?",  # Off-topic
        "response": "To bake a cake, you need flour, eggs, and sugar."
    }
]

async def benchmark(n=100):
    """Run latency benchmark on n requests."""
    pipeline = GuardrailPipeline()
    
    # Generate test queries (repeat scenarios)
    queries = []
    for i in range(n):
        scenario = test_scenarios[i % len(test_scenarios)]
        queries.append((scenario["query"], scenario["response"]))
    
    all_timings = []
    all_results = []
    
    print(f"Running benchmark on {n} requests...")
    for i, (query, response) in enumerate(queries):
        result = await pipeline.full_pipeline_async(query, response)
        all_timings.append(result['timings'])
        all_results.append({
            'query': query[:30],
            'total_latency_ms': result['total_latency_ms'],
            'l1_latency_ms': result['timings'].get('L1', 0),
            'l2_latency_ms': result['timings'].get('L2', 0),
            'l3_latency_ms': result['timings'].get('L3', 0),
            'guardrails_triggered': result['guardrails_triggered']
        })
        
        if (i + 1) % 20 == 0:
            print(f"Progress: {i+1}/{n}")
    
    return all_timings, all_results

if __name__ == "__main__":
    print("Initializing Guardrail Pipeline...")
    
    # Run benchmark
    async def main():
        all_timings, all_results = await benchmark(100)
        
        # Calculate statistics
        import numpy as np
        
        l1_vals = [t.get('L1', 0) for t in all_timings if 'L1' in t]
        l2_vals = [t.get('L2', 0) for t in all_timings if 'L2' in t]
        l3_vals = [t.get('L3', 0) for t in all_timings if 'L3' in t]
        total_vals = [r['total_latency_ms'] for r in all_results]
        
        print(f"\n=== Latency Benchmark Results (100 requests) ===")
        print(f"\nL1 (Input Guards - PII + Topic):")
        print(f"  P50: {np.percentile(l1_vals, 50):.0f}ms")
        print(f"  P95: {np.percentile(l1_vals, 95):.0f}ms")
        print(f"  P99: {np.percentile(l1_vals, 99):.0f}ms")
        
        print(f"\nL2 (RAG Pipeline - Mock):")
        print(f"  P50: {np.percentile(l2_vals, 50):.0f}ms")
        print(f"  P95: {np.percentile(l2_vals, 95):.0f}ms")
        print(f"  P99: {np.percentile(l2_vals, 99):.0f}ms")
        
        print(f"\nL3 (Output Guard - Llama Guard 3):")
        print(f"  P50: {np.percentile(l3_vals, 50):.0f}ms")
        print(f"  P95: {np.percentile(l3_vals, 95):.0f}ms")
        print(f"  P99: {np.percentile(l3_vals, 99):.0f}ms")
        
        print(f"\nTotal End-to-End:")
        print(f"  P50: {np.percentile(total_vals, 50):.0f}ms")
        print(f"  P95: {np.percentile(total_vals, 95):.0f}ms")
        print(f"  P99: {np.percentile(total_vals, 99):.0f}ms")
        
        # Check targets
        print(f"\n=== Target Checks ===")
        l1_p95 = np.percentile(l1_vals, 95)
        l3_p95 = np.percentile(l3_vals, 95)
        
        if l1_p95 < 50:
            print(f"✓ L1 P95 ({l1_p95:.0f}ms) meets target (<50ms)")
        else:
            print(f"✗ L1 P95 ({l1_p95:.0f}ms) above target (<50ms)")
        
        if l3_p95 < 100:
            print(f"✓ L3 P95 ({l3_p95:.0f}ms) meets target (<100ms)")
        else:
            print(f"✗ L3 P95 ({l3_p95:.0f}ms) above target (<100ms)")
        
        # Save results
        import pandas as pd
        results_df = pd.DataFrame(all_results)
        results_df.to_csv("phase-c/latency_benchmark.csv", index=False)
        
        print(f"\n✓ Benchmark complete!")
        print(f"Results saved to phase-c/latency_benchmark.csv")
        
        # Calculate guardrail trigger rates
        topic_triggers = sum(1 for r in all_results if r['guardrails_triggered']['topic'])
        pii_triggers = sum(1 for r in all_results if r['guardrails_triggered']['pii'])
        output_triggers = sum(1 for r in all_results if r['guardrails_triggered']['output'])
        
        print(f"\n=== Guardrail Trigger Rates ===")
        print(f"Topic guard: {topic_triggers/len(all_results):.1%}")
        print(f"PII guard: {pii_triggers/len(all_results):.1%}")
        print(f"Output guard: {output_triggers/len(all_results):.1%}")
    
    asyncio.run(main())
