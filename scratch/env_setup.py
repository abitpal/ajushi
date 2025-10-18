import gymnasium as gym
import numpy as np
import cv2

class CarRacingWrapper:
    """
    Wrapper for the CarRacing-v3 environment:
    - Handles reset and step
    - Converts observations (RGB frames) to grayscale
    - Optionally stacks frames for temporal context
    - Optionally uses continuous or discrete control
    """

    def __init__(self, continuous: bool = True, frame_stack: int = 4, grayscale: bool = True, render_mode: str = None):
        self.env = gym.make("CarRacing-v2", continuous=continuous, render_mode=render_mode)
        self.continuous = continuous
        self.frame_stack = frame_stack
        self.grayscale = grayscale

        obs_shape = self.env.observation_space.shape  # (96, 96, 3)
        self.height, self.width, self.channels = obs_shape

        if grayscale:
            # Grayscale reduces 3 channels → 1
            self.channels = 1

        # Initialize frame buffer for stacking
        self.frames = np.zeros((self.frame_stack, self.height, self.width, self.channels), dtype=np.uint8)

    def preprocess(self, obs):
        """Preprocess the observation (resize, grayscale, normalize)."""
        if self.grayscale:
            obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
            obs = np.expand_dims(obs, -1)  # (H, W, 1)

        # Normalize to [0, 1]
        obs = obs.astype(np.float32) / 255.0
        return obs

    def reset(self, seed=None):
        obs, info = self.env.reset(seed=seed)
        obs = self.preprocess(obs)
        self.frames[:] = obs  # fill all frame stack initially
        return self._get_obs(), info

    def step(self, action):
        next_obs, reward, terminated, truncated, info = self.env.step(action)
        next_obs = self.preprocess(next_obs)

        # Shift frames and append new one
        self.frames = np.roll(self.frames, shift=-1, axis=0)
        self.frames[-1] = next_obs

        done = terminated or truncated
        return self._get_obs(), reward, done, info

    def _get_obs(self):
        """Return stacked observation."""
        return np.concatenate(self.frames, axis=-1)  # (H, W, C * frame_stack)

    def render(self):
        self.env.render()

    def close(self):
        self.env.close()


if __name__ == "__main__":
    env = CarRacingWrapper(continuous=True, frame_stack=4, grayscale=True, render_mode="human")

    obs, info = env.reset()
    done = False
    total_reward = 0.0

    while not done:
        # Sample random actions for demo
        if env.continuous:
            action = np.random.uniform(low=-1.0, high=1.0, size=3)
        else:
            action = env.env.action_space.sample()

        obs, reward, done, info = env.step(action)
        total_reward += reward

        env.render()

    print(f"Episode finished with total reward: {total_reward:.2f}")
    env.close()

