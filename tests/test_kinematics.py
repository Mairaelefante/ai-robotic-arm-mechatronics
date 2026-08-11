import math
import pytest
from src.kinematics import ArmGeometry, forward_kinematics, inverse_kinematics


def test_fk_ik_round_trip():
    arm = ArmGeometry(1.0, 0.8)
    x, y = 1.1, 0.6
    q1, q2 = inverse_kinematics(x, y, arm)
    xr, yr = forward_kinematics(q1, q2, arm)
    assert xr == pytest.approx(x, abs=1e-9)
    assert yr == pytest.approx(y, abs=1e-9)


def test_unreachable_target():
    with pytest.raises(ValueError):
        inverse_kinematics(3.0, 0.0, ArmGeometry())
