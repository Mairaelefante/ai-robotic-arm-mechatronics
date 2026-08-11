import math
from src.kinematics import ArmGeometry, inverse_kinematics, forward_kinematics
from src.simulation import run_simulation


def test_controller_reaches_cartesian_target():
    target_xy = (1.15, 0.75)
    q_target = inverse_kinematics(*target_xy, ArmGeometry())
    result = run_simulation(q_target)
    q = result["angles"][-1]
    xy = forward_kinematics(float(q[0]), float(q[1]), ArmGeometry())
    error = math.hypot(xy[0] - target_xy[0], xy[1] - target_xy[1])
    assert error < 0.04
