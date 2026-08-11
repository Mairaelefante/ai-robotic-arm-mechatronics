from src.control import PID


def test_pid_output_is_limited():
    pid = PID(100.0, 0.0, 0.0, output_limit=2.0)
    assert pid.update(10.0, 0.0, 0.01) == 2.0
