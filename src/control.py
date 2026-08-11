"""Simple PID controller used by the joint simulation."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class PID:
    kp: float
    ki: float
    kd: float
    output_limit: float = 8.0
    integral_limit: float = 4.0
    integral: float = 0.0
    previous_error: float = 0.0

    def reset(self) -> None:
        self.integral = 0.0
        self.previous_error = 0.0

    def update(self, target: float, measured: float, dt: float) -> float:
        error = target - measured
        self.integral += error * dt
        self.integral = max(-self.integral_limit, min(self.integral_limit, self.integral))
        derivative = (error - self.previous_error) / dt if dt > 0 else 0.0
        self.previous_error = error
        output = self.kp * error + self.ki * self.integral + self.kd * derivative
        return max(-self.output_limit, min(self.output_limit, output))
