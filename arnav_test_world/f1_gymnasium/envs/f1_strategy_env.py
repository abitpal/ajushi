from __future__ import annotations

from dataclasses import dataclass
from enum import IntEnum
from typing import Any, Dict, Optional, Tuple

import gymnasium as gym
import numpy as np
from gymnasium import spaces


class TireCompound(IntEnum):
    SOFT = 0
    MEDIUM = 1
    HARD = 2


@dataclass
class TireModel:
    name: str
    performance_offset_s: float  # baseline performance offset (negative is faster)
    wear_per_lap_normal: float   # wear increase per lap at normal pace (0..1)
    wear_penalty_at_full: float  # seconds added when tire_wear == 1.0


class F1StrategyEnv(gym.Env):
    """A simplified single-car F1 strategy environment.

    Objective: minimize total race time via pit timing, tire selection, and pace management.

    Action space (Discrete 6):
        0 = stay out, normal pace
        1 = stay out, push (faster but more wear and ERS usage)
        2 = stay out, save (slower but less wear and builds ERS)
        3 = pit for SOFT
        4 = pit for MEDIUM
        5 = pit for HARD

    Observation space (Dict):
        - lap: int [0, total_laps]
        - stint_laps: int [0, total_laps]
        - tire_compound: {0,1,2}
        - tire_wear: float [0,1]
        - ers: float [0,1]
        - safety_car: {0:none, 1:VSC, 2:SC}

    Reward:
        - Per-step reward is negative lap time in seconds (agent maximizes reward => minimizes time).
        - On pit, pit lane loss is added to the lap time (reduced under SC).
    """

    metadata = {"render_modes": ["ansi"], "render_fps": 4}

    def __init__(
        self,
        render_mode: Optional[str] = None,
        total_laps: int = 50,
        base_lap_time_s: float = 90.0,
        field_variability_s: float = 0.6,
        safety_car_prob: float = 0.03,
        vsc_prob: float = 0.02,
        pit_loss_s: float = 20.0,
        pit_loss_under_sc_s: float = 12.0,
        seed: Optional[int] = None,
    ) -> None:
        assert total_laps > 0
        self.total_laps: int = int(total_laps)
        self.base_lap_time_s: float = float(base_lap_time_s)
        self.field_variability_s: float = float(field_variability_s)
        self.safety_car_prob: float = float(safety_car_prob)
        self.vsc_prob: float = float(vsc_prob)
        self.pit_loss_s: float = float(pit_loss_s)
        self.pit_loss_under_sc_s: float = float(pit_loss_under_sc_s)

        # Tire models
        self.tires: Dict[TireCompound, TireModel] = {
            TireCompound.SOFT: TireModel("soft", performance_offset_s=-1.0, wear_per_lap_normal=0.025, wear_penalty_at_full=3.0),
            TireCompound.MEDIUM: TireModel("medium", performance_offset_s=-0.4, wear_per_lap_normal=0.018, wear_penalty_at_full=2.2),
            TireCompound.HARD: TireModel("hard", performance_offset_s=0.0, wear_per_lap_normal=0.012, wear_penalty_at_full=1.6),
        }

        # Spaces
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.Dict(
            {
                "lap": spaces.Box(low=0, high=self.total_laps, shape=(1,), dtype=np.int32),
                "stint_laps": spaces.Box(low=0, high=self.total_laps, shape=(1,), dtype=np.int32),
                "tire_compound": spaces.Discrete(3),
                "tire_wear": spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32),
                "ers": spaces.Box(low=0.0, high=1.0, shape=(1,), dtype=np.float32),
                "safety_car": spaces.Discrete(3),  # 0 none, 1 VSC, 2 SC
            }
        )

        self.render_mode = render_mode
        self._last_render: Optional[str] = None

        # Internal state
        self.lap: int = 0
        self.stint_laps: int = 0
        self.tire: TireCompound = TireCompound.MEDIUM
        self.tire_wear: float = 0.0
        self.ers: float = 0.7
        self.safety_car_state: int = 0  # 0 none, 1 VSC, 2 SC
        self.total_time_s: float = 0.0

        # RNG
        self.np_random, _ = gym.utils.seeding.np_random(seed)

    def _sample_safety_car(self) -> int:
        # Sample safety car state for the lap (mutually exclusive)
        if self.np_random.random() < self.safety_car_prob:
            return 2  # SC
        if self.np_random.random() < self.vsc_prob:
            return 1  # VSC
        return 0

    def _pace_modifiers(self, action: int) -> Tuple[float, float, float]:
        """Return (lap_time_delta_s, extra_wear, ers_delta)."""
        # Base modifiers for pace modes
        if action == 1:  # push
            return (-0.40, +0.010, -0.12)
        if action == 2:  # save
            return (+0.30, -0.008, +0.08)
        return (0.0, 0.0, -0.02)  # normal

    def _compute_lap_time(self, action: int, pitted: bool) -> float:
        tire_model = self.tires[self.tire]

        # Baseline + compound performance
        lap_time = self.base_lap_time_s + tire_model.performance_offset_s

        # Wear-induced penalty (linear for simplicity)
        lap_time += tire_model.wear_penalty_at_full * np.clip(self.tire_wear, 0.0, 1.0)

        # Pace modifiers
        pace_dt, extra_wear, _ = self._pace_modifiers(action)
        lap_time += pace_dt

        # Field variability / track evolution noise
        lap_time += self.np_random.normal(0.0, self.field_variability_s)

        # Safety car adjustments
        if self.safety_car_state == 2:
            # Full SC: laps are much slower, overtaking restrictions
            lap_time += 13.0
        elif self.safety_car_state == 1:
            # VSC: moderate slowdown
            lap_time += 6.0

        # Pit lane time loss (charged on the lap it happens)
        if pitted:
            lap_time += self.pit_loss_under_sc_s if self.safety_car_state in (1, 2) else self.pit_loss_s

        # Update wear based on pace selection
        wear_increase = tire_model.wear_per_lap_normal + extra_wear
        self.tire_wear = float(np.clip(self.tire_wear + max(wear_increase, 0.0), 0.0, 1.2))

        return float(lap_time)

    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None):  # type: ignore[override]
        super().reset(seed=seed)
        if seed is not None:
            self.np_random, _ = gym.utils.seeding.np_random(seed)

        self.lap = 0
        self.stint_laps = 0
        self.tire = TireCompound.MEDIUM
        self.tire_wear = 0.0
        self.ers = 0.7
        self.safety_car_state = 0
        self.total_time_s = 0.0

        obs = self._get_obs()
        info = {"total_time_s": self.total_time_s}
        self._last_render = self._format_render(info)
        return obs, info

    def step(self, action: int):  # type: ignore[override]
        assert self.action_space.contains(action), "Invalid action"
        terminated = False
        truncated = False

        # Decide pit
        pitted = False
        if action in (3, 4, 5):
            pitted = True
            # Change tire compound
            self.tire = {
                3: TireCompound.SOFT,
                4: TireCompound.MEDIUM,
                5: TireCompound.HARD,
            }[action]
            # Reset stint
            self.stint_laps = 0
            self.tire_wear = 0.0
            # After changing compound, pace part of action becomes "normal" for this lap time computation
            # We still use the action for ERS delta (handled below via _pace_modifiers), but treat pace as normal for simplicity.

        # Sample safety car state for this lap
        self.safety_car_state = self._sample_safety_car()

        # Compute lap time and update wear
        lap_time_s = self._compute_lap_time(action if action in (0, 1, 2) else 0, pitted)
        self.total_time_s += lap_time_s

        # ERS dynamics
        _, _, ers_delta = self._pace_modifiers(action if action in (0, 1, 2) else 0)
        # Regenerate a little more ERS under SC conditions
        if self.safety_car_state == 2:
            ers_delta += 0.08
        elif self.safety_car_state == 1:
            ers_delta += 0.04
        self.ers = float(np.clip(self.ers + ers_delta, 0.0, 1.0))

        # Advance lap counters
        self.lap += 1
        if not pitted:
            self.stint_laps += 1

        # Episode termination when race distance completed
        if self.lap >= self.total_laps:
            terminated = True

        reward = -lap_time_s
        obs = self._get_obs()
        info = {
            "lap_time_s": lap_time_s,
            "total_time_s": self.total_time_s,
            "pitted": pitted,
            "tire": self.tires[self.tire].name,
            "safety_car_state": self.safety_car_state,
        }

        self._last_render = self._format_render(info)
        return obs, reward, terminated, truncated, info

    def _get_obs(self) -> Dict[str, Any]:
        return {
            "lap": np.array([self.lap], dtype=np.int32),
            "stint_laps": np.array([self.stint_laps], dtype=np.int32),
            "tire_compound": int(self.tire),
            "tire_wear": np.array([np.clip(self.tire_wear, 0.0, 1.0)], dtype=np.float32),
            "ers": np.array([self.ers], dtype=np.float32),
            "safety_car": int(self.safety_car_state),
        }

    def _format_render(self, last_info: Optional[Dict[str, Any]]) -> str:
        tire_name = self.tires[self.tire].name
        return (
            f"Lap {self.lap}/{self.total_laps} | Stint {self.stint_laps} | Tire {tire_name} "
            f"wear {self.tire_wear:.2f} | ERS {self.ers:.2f} | SC {self.safety_car_state} | "
            f"total {self.total_time_s:.2f}s"
            + ("" if not last_info else f" | lap {last_info.get('lap_time_s', 0.0):.2f}s")
        )

    def render(self) -> Optional[str]:  # type: ignore[override]
        if self.render_mode == "ansi":
            return self._last_render or ""
        return None

    def close(self) -> None:  # type: ignore[override]
        # Nothing to clean up for ansi rendering
        return None


