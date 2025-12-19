import sys
import os
import random

# Add parent directory to path to import src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.nei import NEICalculator, NEIMetrics

def main():
    print("--- Example 3: Node Health Dashboard Check ---")
    
    nodes = {
        "QueryRewriter":  {"lat": 0.2, "tok": 100, "qual": 0.8},
        "VectorStore":    {"lat": 0.5, "tok": 0,   "qual": 0.9}, # Pure retrieval
        "Summarizer":     {"lat": 2.0, "tok": 1000,"qual": 0.85}
    }
    
    # Simulated proposed changes (e.g., trying a larger model for Rewriter, caching for VectorStore)
    candidates = {
        "QueryRewriter":  {"lat": 0.4, "tok": 300, "qual": 0.82}, # Bigger model: slower, expensive, slightly better
        "VectorStore":    {"lat": 0.1, "tok": 0,   "qual": 0.90}, # Caching: faster, same quality
        "Summarizer":     {"lat": 1.0, "tok": 500, "qual": 0.84}  # Quantized: faster, cheaper, slightly worse qual
    }
    
    calc = NEICalculator(alpha=0.4, beta=0.2, gamma=0.4) # Time and Quality are important
    
    print(f"{'Node':<15} | {'Score':<10} | {'Verdict':<15}")
    print("-" * 45)
    
    for name, base_data in nodes.items():
        cand_data = candidates[name]
        
        b = NEIMetrics(base_data["lat"], base_data["tok"], base_data["qual"])
        c = NEIMetrics(cand_data["lat"], cand_data["tok"], cand_data["qual"])
        
        res = calc.calculate(b, c)
        
        score_color = ""
        if res.efficiency_score > 0:
            status = "✅ KEEP"
        else:
            status = "❌ REJECT"
            
        print(f"{name:<15} | {res.efficiency_score:>6.2f}     | {status}")

    print("-" * 45)
    print("Summary:")
    print("1. QueryRewriter: Rejected. 2% quality gain didn't justify 2x latency/3x cost.")
    print("2. VectorStore:   Accepted. Optimization (Caching) reduced latency by 80%.")
    print("3. Summarizer:    Accepted. Optimization. Quality dropped 1%, but Speed/Cost improved 50%. Win.")

if __name__ == "__main__":
    main()
