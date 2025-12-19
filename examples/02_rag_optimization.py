import sys
import os

# Add parent directory to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nei import NEICalculator, NEIMetrics

def main():
    print("--- Example 2: RAG Optimization (Adding Re-ranker) ---")
    
    # Scene: Improving RAG pipeline.
    # Adding a Cross-Encoder Re-ranker increases latency significantly, cost slightly, but usually helps quality.
    
    baseline = NEIMetrics(latency=0.8, tokens=500, quality=0.65)
    rerank_node = NEIMetrics(latency=1.4, tokens=550, quality=0.82)
    
    # Balanced weights
    calc = NEICalculator(alpha=0.33, beta=0.33, gamma=0.34)
    
    result = calc.calculate(baseline, rerank_node)
    
    print(f"Delta Quality: {result.delta_quality:+.1%}")
    print(f"Delta Latency: {result.delta_latency:+.1%}")
    
    print(f"\nNEI Index: {result.nei_index:.2f}")
    print(f"Efficiency Score: {result.efficiency_score:.2f}")
    print(f"Verdict: {result.explanation}")
    
    if result.efficiency_score > 0:
        print("\nConclusion: Success! The re-ranker is inefficient latency-wise, but the quality jump compensates.")
    else:
        print("\nConclusion: Failure. Too slow for the quality gained.")

if __name__ == "__main__":
    main()
