"""Closed-loop two-joint mechatronic simulation."""
from __future__ import annotations
from dataclasses import dataclass
import numpy as np
from .control import PID
from .kinematics import ArmGeometry, forward_kinematics
from .sensors import JointSensor, detect_tracking_fault


@dataclass
class SimulationConfig:
    dt: float = 0.01
    duration: float = 6.0
    inertia: float = 1.0
    damping: float = 1.3
    max_velocity: float = 3.0


def smooth_step(t: float, duration: float, start: np.ndarray, target: np.ndarray) -> np.ndarray:
    u = max(0.0, min(1.0, t / duration))
    s = u * u * (3.0 - 2.0 * u)
    return start + s * (target - start)


def run_simulation(target_angles: tuple[float, float], config: SimulationConfig | None = None):
    cfg = config or SimulationConfig()
    steps = int(cfg.duration / cfg.dt) + 1
    times = np.linspace(0.0, cfg.duration, steps)
    q = np.zeros(2, dtype=float)
    dq = np.zeros(2, dtype=float)
    target = np.asarray(target_angles, dtype=float)
    controllers = [PID(14.0, 0.5, 2.2), PID(14.0, 0.5, 2.2)]
    sensors = [JointSensor(seed=11), JointSensor(seed=23)]
    arm = ArmGeometry()

    q_log, measured_log, target_log, xy_log, fault_log = [], [], [], [], []
    for t in times:
        desired = smooth_step(t, min(2.0, cfg.duration / 2.0), np.zeros(2), target)
        measured = np.array([sensors[i].read(q[i]) for i in range(2)])
        torque = np.array([controllers[i].update(desired[i], measured[i], cfg.dt) for i in range(2)])
        ddq = (torque - cfg.damping * dq) / cfg.inertia
        dq += ddq * cfg.dt
        dq = np.clip(dq, -cfg.max_velocity, cfg.max_velocity)
        q += dq * cfg.dt
        xy = forward_kinematics(float(q[0]), float(q[1]), arm)
        faults = [detect_tracking_fault(float(desired[i]), float(measured[i])) for i in range(2)]
        q_log.append(q.copy()); measured_log.append(measured); target_log.append(desired.copy())
        xy_log.append(xy); fault_log.append(faults)

    return {
        "time": times,
        "angles": np.asarray(q_log),
        "measured": np.asarray(measured_log),
        "targets": np.asarray(target_log),
        "xy": np.asarray(xy_log),
        "faults": np.asarray(fault_log, dtype=bool),
    }
