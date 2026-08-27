"""
submission.py

AgriMind AI Kaggriculture submission entry point.

Architecture
------------

    Kaggriculture
          |
          v
    submission.run()
          |
          v
       main.agent()
          |
          v
    core.parser
          |
          v
      GameState
          |
          v
   StrategicAgent
          |
          v
   Internal Action
          |
          v
       actions
          |
          v
 Kaggriculture Action

This file intentionally contains no game logic.

All parsing, state construction, decision making, memory,
economy, planning, risk analysis, and action conversion belong
to the internal AgriMind architecture.
"""

from typing import Any

from main import agent


# ============================================================
# Public Submission API
# ============================================================

def run(observation: dict) -> dict:
    """
    Execute AgriMind AI for one Kaggriculture observation.

    Parameters
    ----------
    observation:
        Raw observation supplied by the Kaggriculture environment.

    Returns
    -------
    dict
        Kaggriculture-compatible action.
    """

    return agent(observation)


# ============================================================
# Standard Agent Alias
# ============================================================

my_agent = run


# ============================================================
# Optional Compatibility Entry Point
# ============================================================

def submit(observation: dict) -> dict:
    """
    Compatibility wrapper for environments or local tooling
    that use a `submit` function name.
    """

    return run(observation)


# ============================================================
# Local Smoke Test
# ============================================================

def smoke_test() -> dict:
    """
    Run a minimal end-to-end smoke test.

    The observation is deliberately small. The real parser is
    responsible for handling the complete Kaggriculture schema.
    """

    observation: dict[str, Any] = {
        "step": 0,
        "player": 0,
        "day": 0,
        "hour": 0,
    }

    result = run(observation)

    if not isinstance(result, dict):
        raise TypeError(
            "Agent must return a dictionary."
        )

    if "farmer" not in result:
        raise ValueError(
            "Agent result is missing the 'farmer' field."
        )

    if "market" not in result:
        raise ValueError(
            "Agent result is missing the 'market' field."
        )

    return result


# ============================================================
# Local Execution
# ============================================================

if __name__ == "__main__":

    result = smoke_test()

    print("Submission smoke test: OK")
    print("Agent output:")
    print(result)