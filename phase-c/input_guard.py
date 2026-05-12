"""
Phase C.1 - Input Guardrail: PII Redaction
Implement PII detection and redaction using Presidio + custom VN regex
"""

import re
import time
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

VN_PII = {
    "cccd": r"\b\d{12}\b",  # Citizen ID
    "phone_vn": r"(\+84|0)\d{9,10}",
    "tax_code": r"\b\d{10}(-\d{3})?\b",
    "email": r"\b[\w.-]+@[\w.-]+\.\w+\b",
}

class InputGuard:
    def __init__(self):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()

    def scrub_vn(self, t):
        """Layer 1: VN-specific regex."""
        found_pii = []
        for name, pattern in VN_PII.items():
            matches = re.findall(pattern, t)
            if matches:
                found_pii.extend([name] * len(matches))
            t = re.sub(pattern, f" [{name.upper()}]", t)
        return t, found_pii

    def scrub_ner(self, t):
        """Layer 2: Presidio NER (multilingual)."""
        try:
            results = self.analyzer.analyze(text=t, language="en")
            anonymized = self.anonymizer.anonymize(text=t, analyzer_results=results)
            return anonymized.text, [r.entity_type for r in results]
        except Exception as e:
            # Fallback if Presidio fails
            return t, []

    def sanitize(self, t):
        """Full pipeline with latency tracking."""
        start = time.perf_counter()
        
        # Layer 1: VN regex
        t, vn_pii = self.scrub_vn(t)
        
        # Layer 2: Presidio NER
        t, ner_pii = self.scrub_ner(t)
        
        latency_ms = (time.perf_counter() - start) * 1000
        all_pii = vn_pii + ner_pii
        return t, all_pii, latency_ms

# Test set
test_inputs = [
    # English NER
    "Hi, I'm John Smith from Microsoft. Email: john@ms.com",
    "Call me at +1-555-1234 or visit 123 Main Street, NYC",
    # VN regex
    "Số CCCD của tôi là 012345678901",
    "Liên hệ qua 0987654321 hoặc tax 0123456789-001",
    # Mixed
    "Customer Nguyễn Văn A, CCCD 098765432101, phone 0912345678",
    # Edge cases
    "Just a normal question",  # No PII
    "A" * 5000,  # Very long
    "Lý Văn Bình ở 123 Lê Lợi",  # Vietnamese name (Presidio EN may miss)
    "tax_code: 0123456789-001 cccd:012345678901",  # Multiple PII
    "My email is test@example.com and phone is 0901234567",  # Mixed EN/VN
]

if __name__ == "__main__":
    print("Initializing Input Guard...")
    guard = InputGuard()
    
    print("Running PII detection tests...")
    results = []
    for idx, test_input in enumerate(test_inputs):
        output, pii_found, latency = guard.sanitize(test_input)
        
        results.append({
            'input': test_input[:100],
            'output': output[:100],
            'pii_found': ', '.join(pii_found) if pii_found else 'None',
            'latency_ms': round(latency, 2),
            'has_pii': len(pii_found) > 0
        })
        
        print(f"[{idx+1}/10] PII found: {len(pii_found)}, Latency: {latency:.2f}ms")
    
    # Save results
    import pandas as pd
    results_df = pd.DataFrame(results)
    results_df.to_csv("phase-c/pii_test_results.csv", index=False)
    
    print(f"\n✓ PII testing complete!")
    print(f"Results saved to phase-c/pii_test_results.csv")
    
    # Calculate metrics
    detection_rate = results_df['has_pii'].sum() / len(results_df)
    avg_latency = results_df['latency_ms'].mean()
    p95_latency = results_df['latency_ms'].quantile(0.95)
    
    print(f"\n=== Metrics ===")
    print(f"Detection rate: {detection_rate:.1%}")
    print(f"Average latency: {avg_latency:.2f}ms")
    print(f"P95 latency: {p95_latency:.2f}ms")
    
    if detection_rate >= 0.8:
        print("✓ Detection rate meets target (≥80%)")
    else:
        print("✗ Detection rate below target (≥80%)")
    
    if p95_latency < 50:
        print("✓ P95 latency meets target (<50ms)")
    else:
        print("✗ P95 latency above target (<50ms)")
