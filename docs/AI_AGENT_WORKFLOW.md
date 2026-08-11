# AI Coding Agent Workflow

## Purpose

This document provides a reproducible record of how an AI coding agent can be used on a robotics/mechatronics software task without treating generated code as automatically correct.

## 1. Engineering task

Build a two-joint planar robotic-arm simulation that accepts a Cartesian target and performs the complete sequence from inverse kinematics to closed-loop motion and verification.

## 2. Agent responsibilities

The coding agent can be asked to:

- create the multi-file project structure;
- implement analytical forward/inverse kinematics;
- implement PID control and simplified joint dynamics;
- add sensor noise and fault-detection logic;
- write automated tests;
- investigate failing tests and propose corrections;
- improve documentation after implementation.

## 3. Human responsibilities

The engineer should independently verify:

- kinematic equations and coordinate conventions;
- workspace/reachability handling;
- numerical stability and time-step assumptions;
- controller saturation and convergence;
- whether tests measure meaningful physical/software behaviour;
- that documentation distinguishes simulation assumptions from real hardware claims.

## 4. Example agent sequence

1. Ask the agent to propose modules and interfaces before coding.
2. Ask it to implement kinematics plus unit tests first.
3. Run tests and inspect equations manually.
4. Add controller and plant simulation in a second change.
5. Run the end-to-end target test.
6. If convergence fails, provide the test output and ask the agent to diagnose rather than simply loosen the assertion.
7. Review the proposed change, rerun all tests, and inspect the final trajectory.
8. Record the failure, diagnosis, correction, and verification result.

## 5. Example evaluation record

| Stage | Evidence to record |
|---|---|
| Task context | Required target, assumptions, acceptance criteria |
| Agent instruction | Exact engineering request given to the coding agent |
| Generated change | Files/functions created or modified |
| Failure | Test output, numerical error, or unexpected trajectory |
| Diagnosis | Agent hypothesis plus independent engineering review |
| Correction | Accepted/rejected code changes and why |
| Verification | Test results and quantitative final error |

## 6. Interview-safe description

This repository demonstrates AI-assisted engineering in simulation. The AI agent accelerates implementation and debugging, while equations, assumptions, tests, and final behaviour are reviewed and validated by the human developer. It should not be described as experience deploying a physical industrial robot.
