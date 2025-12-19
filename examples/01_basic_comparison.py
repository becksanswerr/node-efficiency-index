import sys
import os

# Add parent directory to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nei import NEICalculator, NEIMetrics

def main():
    print("--- Example 1: Basic Comparison (Model A vs Model B) ---")
    
    # Scene: Switching from GPT-3.5 (Baseline) to GPT-4 (Candidate)
    # GPT-4 is slower and more expensive, but smarter.
    
    baseline = NEIMetrics(latency=1.5, tokens=0.002, quality=0.80)
    candidate = NEIMetrics(latency=3.0, tokens=0.030, quality=0.85) # 15x cost, 2x latency
    
    # We are very price sensitive here
    calc = NEICalculator(alpha=0.2, beta=0.6, gamma=0.2) 
    
    result = calc.calculate(baseline, candidate)
    
    print(f"Baseline Quality: {baseline.quality} | Cost: ${baseline.tokens}")
    print(f"Candidate Quality: {candidate.quality} | Cost: ${candidate.tokens}")
    print(f"\nDelta Quality: {result.delta_quality:+.1%}")
    print(f"Delta Cost:    {result.delta_tokens:+.1%}")
    print(f"Delta Latency: {result.delta_latency:+.1%}")
    
    print(f"\nNEI Efficiency Score: {result.efficiency_score:.2f}")
    print(f"Verdict: {result.explanation}")
    
    if result.efficiency_score < 0:
        print("\nConclusion: The quality boost is too small to justify the massive cost increase.")

if __name__ == "__main__":
    main()
