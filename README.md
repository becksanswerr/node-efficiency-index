# Node Efficiency Index (NEI)

**A Unified Metric for Evaluating LLM Workflow Nodes**

![License](https://img.shields.io/badge/license-MIT-blue)
![Python](https://img.shields.io/badge/python-3.8%2B-green)

The **Node Efficiency Index (NEI)** is a framework and metric designed to help AI Engineers answer the question: *"Is adding this new node to my LangChain/LangGraph workflow worth the extra latency and cost?"*

## 📄 The Paper

[Read the full theoretical paper here](./paper/NEI_Main_Paper.md)

## 🚀 Quick Start

### Installation

Clone the repository:

```bash
git clone https://github.com/your-username/node-efficiency-index.git
cd node-efficiency-index
```

### Usage

```python
from src.nei import NEICalculator, NEIMetrics

# 1. Define your Baseline (Current System)
baseline = NEIMetrics(
    latency=1.2,  # seconds
    tokens=800,   # count
    quality=0.75  # 0.0-1.0 score (from DeepEval/Ragas)
)

# 2. Define your Candidate (New System with extra node)
candidate = NEIMetrics(
    latency=1.8,
    tokens=850,
    quality=0.88
)

# 3. Calculate Efficiency with custom weights
# alpha=Time, beta=Cost, gamma=Quality
calc = NEICalculator(alpha=0.33, beta=0.33, gamma=0.34)
result = calc.calculate(baseline, candidate)

print(f"Efficiency Score: {result.efficiency_score:.2f}")
print(f"Verdict: {result.explanation}")
```

## 📂 Examples

Check the `examples/` folder for runnable scenarios:

- `01_basic_comparison.py`: Simple Baseline vs Candidate check.
- `02_rag_optimization.py`: Evaluating a Re-ranking node in a RAG pipeline.

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a PR.

## 📜 License

MIT License.
