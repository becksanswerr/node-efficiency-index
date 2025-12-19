from dataclasses import dataclass
from typing import Dict, Optional
import logging

@dataclass
class NEIMetrics:
    """
    Data class representing the metrics for a node or workflow state.
    
    Attributes:
        latency (float): Execution time in seconds.
        tokens (float): Generic Cost Metric. Can be Token Usage (count) or Dollar Cost ($).
        quality (float): Quality score (0.0 to 1.0).
    """
    latency: float
    tokens: float
    quality: float

@dataclass
class NEIResult:
    """
    Result of an NEI calculation.
    """
    efficiency_score: float
    nei_index: float
    delta_latency: float
    delta_tokens: float
    delta_quality: float
    is_efficient: bool
    explanation: str

class NEICalculator:
    """
    Calculator for Node Efficiency Index (NEI).
    """
    def __init__(self, alpha: float = 0.33, beta: float = 0.33, gamma: float = 0.34):
        """
        Initialize with user-defined sensitivity weights.
        
        Args:
            alpha (float): Sensitivity to Latency (Time).
            beta (float): Sensitivity to Cost (Tokens/Dollars).
            gamma (float): Sensitivity to Quality.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        # Optionally warn if weights are significantly off 1.0, but do not enforce.
        total_weight = alpha + beta + gamma
        if not (0.9 <= total_weight <= 1.1):
            logging.warning(
                f"Weights sum to {total_weight}, which is far from 1.0. "
                "Ensure this is intentional for your custom scoring normalization."
            )

    def calculate(self, baseline: NEIMetrics, candidate: NEIMetrics) -> NEIResult:
        """
        Calculate NEI comparing a Candidate state against a Baseline.
        """
        # Calculate Deltas (Normalized percentage change)
        # Avoid division by zero by using a small epsilon if baseline is 0
        epsilon = 1e-9
        
        d_T = (candidate.latency - baseline.latency) / (baseline.latency + epsilon)
        d_N = (candidate.tokens - baseline.tokens) / (baseline.tokens + epsilon)
        d_Q = (candidate.quality - baseline.quality) / (baseline.quality + epsilon)

        # General Efficiency Score (Weighted Net Benefit)
        # Formula: (gamma * dQ - alpha * dT - beta * dN) * 100
        efficiency_score = (self.gamma * d_Q - self.alpha * d_T - self.beta * d_N) * 100

        # NEI Index (Ratio)
        # We handle "Optimization" (negative cost/latency) vs "Expansion" (positive cost/latency)
        
        cost_impact = (self.alpha * d_T) + (self.beta * d_N)
        
        if cost_impact > 0:
            # Expansion Case: We paid more. Did we get enough Quality?
            nei_index = d_Q / (cost_impact + epsilon)
        else:
            # Optimization Case: We paid less.
            # If d_Q is positive, it's Infinite efficiency (Win-Win).
            # If d_Q is negative (quality dropped), we check if the cost saving was worth it.
            # For simplicity in this scalar implementation, we stick to the Efficiency Score for decision making
            # but return a distinct value for NEI.
            if d_Q >= 0:
                nei_index = float('inf') # Pure Win
            else:
                nei_index = d_Q / (cost_impact + epsilon) # Both are negative, ratio is positive

        is_efficient = efficiency_score > 0
        
        explanation = "Efficient" if is_efficient else "Inefficient"
        if is_efficient:
            explanation += f": Quality gain ({d_Q:.1%}) justifies correlation of cost increase."
        else:
            explanation += f": Cost/Latency penalty outweighs Quality gain ({d_Q:.1%})."

        return NEIResult(
            efficiency_score=efficiency_score,
            nei_index=nei_index,
            delta_latency=d_T,
            delta_tokens=d_N,
            delta_quality=d_Q,
            is_efficient=is_efficient,
            explanation=explanation
        )
