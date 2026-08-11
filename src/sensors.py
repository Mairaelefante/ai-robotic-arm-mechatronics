"""Sensor models and basic fault detection."""
from __future__ import annotations
import numpy as np


class JointSensor:
    def __init__(self, noise_std: float = 0.004, bias: float = 0.0, seed: int = 7):
        self.noise_std = noise_std
        self.bias = bias
        self.rng = np.random.default_rng(seed)

    def read(self, true_angle: float) -> float:
        return float(true_angle + self.bias + self.rng.normal(0.0, self.noise_std))


def detect_tracking_fault(target: float, measured: float, threshold: float = 0.12) -> bool:
    """Flag a persistent-sized joint tracking discrepancy."""
    return abs(target - measured) > threshold
