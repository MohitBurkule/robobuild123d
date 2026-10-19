"""A screw threaded into a motor's tap hole must still link the stator, so the bell-rub sweep skips it."""
import inspect

from robot.checks import kinematics


def test_declared_thread_target_falls_back_to_shank_tip():
    src = inspect.getsource(kinematics)
    assert "f.threads_into == m" in src
