from gymnasium.envs.registration import register

# Re-export envs for direct import if desired
from .envs import F1StrategyEnv  # noqa: F401


# Register the environment with Gymnasium on import
register(
    id="f1_gymnasium/F1Strategy-v0",
    entry_point="f1_gymnasium.envs:F1StrategyEnv",
)


