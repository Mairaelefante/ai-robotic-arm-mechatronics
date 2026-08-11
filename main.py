"""Run an inverse-kinematics target followed by closed-loop control."""
import argparse
import math
import matplotlib.pyplot as plt
from src.kinematics import ArmGeometry, inverse_kinematics, forward_kinematics
from src.simulation import run_simulation


def main():
    parser = argparse.ArgumentParser(description="AI-assisted robotic arm mechatronics simulation")
    parser.add_argument("--x", type=float, default=1.15, help="Target x position")
    parser.add_argument("--y", type=float, default=0.75, help="Target y position")
    parser.add_argument("--no-plot", action="store_true", help="Run without opening plots")
    args = parser.parse_args()

    arm = ArmGeometry()
    target_angles = inverse_kinematics(args.x, args.y, arm, elbow_up=False)
    result = run_simulation(target_angles)
    final_angles = result["angles"][-1]
    final_xy = forward_kinematics(float(final_angles[0]), float(final_angles[1]), arm)
    error = math.hypot(final_xy[0] - args.x, final_xy[1] - args.y)

    print(f"Cartesian target: ({args.x:.3f}, {args.y:.3f})")
    print(f"IK joint target: ({target_angles[0]:.3f}, {target_angles[1]:.3f}) rad")
    print(f"Final position:   ({final_xy[0]:.3f}, {final_xy[1]:.3f})")
    print(f"Position error:   {error:.5f}")
    print(f"Fault samples:    {int(result['faults'].sum())}")

    if not args.no_plot:
        t = result["time"]
        plt.figure()
        plt.plot(t, result["targets"][:, 0], label="joint 1 target")
        plt.plot(t, result["angles"][:, 0], label="joint 1 actual")
        plt.plot(t, result["targets"][:, 1], label="joint 2 target")
        plt.plot(t, result["angles"][:, 1], label="joint 2 actual")
        plt.xlabel("Time [s]"); plt.ylabel("Angle [rad]"); plt.legend(); plt.tight_layout()

        plt.figure()
        plt.plot(result["xy"][:, 0], result["xy"][:, 1])
        plt.scatter([args.x], [args.y], marker="x", label="target")
        plt.xlabel("x"); plt.ylabel("y"); plt.axis("equal"); plt.legend(); plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    main()
