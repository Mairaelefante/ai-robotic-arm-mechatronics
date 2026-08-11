"""Forward and inverse kinematics for a planar two-link robotic arm."""
from __future__ import annotations
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ArmGeometry:
    link1: float = 1.0
    link2: float = 0.8


def forward_kinematics(theta1: float, theta2: float, arm: ArmGeometry) -> tuple[float, float]:
    """Return end-effector (x, y) for joint angles in radians."""
    x = arm.link1 * math.cos(theta1) + arm.link2 * math.cos(theta1 + theta2)
    y = arm.link1 * math.sin(theta1) + arm.link2 * math.sin(theta1 + theta2)
    return x, y


def inverse_kinematics(x: float, y: float, arm: ArmGeometry, elbow_up: bool = False) -> tuple[float, float]:
    """Solve planar 2-link IK. Raises ValueError when target is unreachable."""
    r2 = x * x + y * y
    c2 = (r2 - arm.link1**2 - arm.link2**2) / (2.0 * arm.link1 * arm.link2)
    if c2 < -1.0 - 1e-12 or c2 > 1.0 + 1e-12:
        raise ValueError(f"Target ({x:.3f}, {y:.3f}) is outside the workspace")
    c2 = max(-1.0, min(1.0, c2))
    s2_mag = math.sqrt(max(0.0, 1.0 - c2 * c2))
    s2 = s2_mag if elbow_up else -s2_mag
    theta2 = math.atan2(s2, c2)
    theta1 = math.atan2(y, x) - math.atan2(arm.link2 * s2, arm.link1 + arm.link2 * c2)
    return theta1, theta2
