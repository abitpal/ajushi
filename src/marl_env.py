import gymnasium as gym
import numpy as np
import cv2
from typing import Any, Tuple, Optional, Dict, List, Union
from gymnasium import spaces
import pygame
# from gymnasium.wrappers import FrameStack, GrayScaleObservation, ResizeObservation

class MultiAgentCarRacingEnv(gym.Env):
    """
    Multi-Agent Car Racing Environment
    
    This environment supports multiple agents racing simultaneously on the same track.
    Each agent has its own observation space and can take independent actions.
    """
    
    metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 50}
    
    def __init__(
        self, 
        n_agents: int = 2,
        continuous: bool = True, 
        frame_stack: int = 4, 
        grayscale: bool = True, 
        render_mode: str = None,
        track_length: int = 1000,
        collision_penalty: float = -10.0,
        cooperation_reward: float = 1.0
    ):
        super().__init__()
        
        self.n_agents = n_agents
        self.continuous = continuous
        self.frame_stack = frame_stack
        self.grayscale = grayscale
        self.render_mode = render_mode
        self.track_length = track_length
        self.collision_penalty = collision_penalty
        self.cooperation_reward = cooperation_reward
        
        # Create individual environments for each agent
        self.envs = []
        for i in range(n_agents):
            env = gym.make("CarRacing-v3", continuous=continuous, render_mode=render_mode)
            self.envs.append(env)
        
        # Get observation and action spaces from first environment
        base_obs_shape = self.envs[0].observation_space.shape  # (96, 96, 3)
        self.height, self.width, self.channels = base_obs_shape
        
        if grayscale:
            self.channels = 1
        
        # DQN expects 84x84 images, so we'll resize from 96x96 to 84x84
        self.dqn_height, self.dqn_width = 84, 84
        
        # Initialize frame buffers for each agent - use 84x84 for DQN compatibility
        self.frames = np.zeros((n_agents, self.frame_stack, self.dqn_height, self.dqn_width, self.channels), dtype=np.float32)
        
        # Define multi-agent observation space - use 84x84 for DQN compatibility
        if grayscale:
            obs_shape = (self.frame_stack, self.dqn_height, self.dqn_width)
        else:
            obs_shape = (self.frame_stack * 3, self.dqn_height, self.dqn_width)
            
        # Multi-agent observation space: list of individual observation spaces
        self.observation_space = spaces.Tuple([
            spaces.Box(low=0.0, high=1.0, shape=obs_shape, dtype=np.float32)
            for _ in range(n_agents)
        ])
        
        # Multi-agent action space: list of individual action spaces
        if continuous:
            self.action_space = spaces.Tuple([
                spaces.Box(low=-1.0, high=1.0, shape=(3,), dtype=np.float32)
                for _ in range(n_agents)
            ])
        else:
            self.action_space = spaces.Tuple([
                self.envs[0].action_space for _ in range(n_agents)
            ])
        
        # Agent states
        self.agent_positions = np.zeros((n_agents, 2))  # x, y positions
        self.agent_velocities = np.zeros((n_agents, 2))  # vx, vy velocities
        self.agent_angles = np.zeros(n_agents)  # heading angles
        self.agent_rewards = np.zeros(n_agents)
        self.agent_dones = np.zeros(n_agents, dtype=bool)
        self.agent_infos = [{} for _ in range(n_agents)]
        
        # Track progress
        self.track_progress = np.zeros(n_agents)
        self.last_positions = np.zeros((n_agents, 2))
        
    def preprocess(self, obs, agent_id):
        """Preprocess observation for a specific agent."""
        # Resize from 96x96 to 84x84 to match DQN expectations FIRST
        obs = cv2.resize(obs, (self.dqn_width, self.dqn_height), interpolation=cv2.INTER_AREA)
        
        if self.grayscale:
            obs = cv2.cvtColor(obs, cv2.COLOR_RGB2GRAY)
            obs = np.expand_dims(obs, -1)  # (H, W, 1)
        
        # Normalize to [0, 1]
        obs = obs.astype(np.float32) / 255.0
        return obs
    
    def reset(self, seed: Optional[int] = None, options: Optional[Dict[str, Any]] = None) -> Tuple[List[np.ndarray], Dict[str, Any]]:
        """Reset all agent environments."""
        observations = []
        
        for i, env in enumerate(self.envs):
            obs, info = env.reset(seed=seed + i if seed is not None else None, options=options)
            obs = self.preprocess(obs, i)
            self.frames[i, :] = obs  # Fill frame stack initially
            self.agent_infos[i] = info
            
            # Get stacked observation in (C, H, W) format
            stacked_obs = self._get_obs(i)
            observations.append(np.transpose(stacked_obs, (2, 0, 1)))
        
        # Reset agent states
        self.agent_positions.fill(0)
        self.agent_velocities.fill(0)
        self.agent_angles.fill(0)
        self.agent_rewards.fill(0)
        self.agent_dones.fill(False)
        self.track_progress.fill(0)
        self.last_positions.fill(0)
        
        return observations, {"agent_infos": self.agent_infos}
    
    def step(self, actions: List[np.ndarray]) -> Tuple[List[np.ndarray], List[float], List[bool], List[bool], Dict[str, Any]]:
        """Step all agents simultaneously."""
        observations = []
        rewards = []
        terminateds = []
        truncateds = []
        
        # Step each agent
        for i, (env, action) in enumerate(zip(self.envs, actions)):
            if not self.agent_dones[i]:
                obs, reward, terminated, truncated, info = env.step(action)
                obs = self.preprocess(obs, i)
                
                # Update frame stack
                self.frames[i] = np.roll(self.frames[i], shift=-1, axis=0)
                self.frames[i, -1] = obs
                
                # Update agent state
                self.agent_rewards[i] = reward
                self.agent_dones[i] = terminated or truncated
                self.agent_infos[i] = info
                
                # Get stacked observation
                stacked_obs = self._get_obs(i)
                observations.append(np.transpose(stacked_obs, (2, 0, 1)))
                rewards.append(reward)
                terminateds.append(terminated)
                truncateds.append(truncated)
            else:
                # Agent is done, return zero observation and reward
                stacked_obs = self._get_obs(i)
                observations.append(np.transpose(stacked_obs, (2, 0, 1)))
                rewards.append(0.0)
                terminateds.append(True)
                truncateds.append(False)
        
        # Calculate multi-agent rewards (collision penalties, cooperation bonuses)
        multi_agent_rewards = self._calculate_multi_agent_rewards(rewards)
        
        # Check if all agents are done
        all_done = all(self.agent_dones)
        
        return observations, multi_agent_rewards, terminateds, truncateds, {"agent_infos": self.agent_infos}
    
    def _get_obs(self, agent_id):
        """Get stacked observation for a specific agent."""
        return np.concatenate(self.frames[agent_id], axis=-1)  # (H, W, C * frame_stack)
    
    def _calculate_multi_agent_rewards(self, individual_rewards):
        """Calculate multi-agent rewards including collision penalties and cooperation bonuses."""
        multi_agent_rewards = individual_rewards.copy()
        
        # Add collision penalties
        for i in range(self.n_agents):
            for j in range(i + 1, self.n_agents):
                if self._agents_collide(i, j):
                    multi_agent_rewards[i] += self.collision_penalty
                    multi_agent_rewards[j] += self.collision_penalty
        
        # Add cooperation bonuses (agents close to each other get bonus)
        for i in range(self.n_agents):
            for j in range(i + 1, self.n_agents):
                distance = np.linalg.norm(self.agent_positions[i] - self.agent_positions[j])
                if distance < 50:  # Close proximity threshold
                    multi_agent_rewards[i] += self.cooperation_reward
                    multi_agent_rewards[j] += self.cooperation_reward
        
        return multi_agent_rewards
    
    def _agents_collide(self, agent1_id, agent2_id):
        """Check if two agents are colliding."""
        distance = np.linalg.norm(self.agent_positions[agent1_id] - self.agent_positions[agent2_id])
        return distance < 20  # Collision threshold

    def render(self, stuff, mode="human"):
        """Render all agents on a single combined frame."""
        
        # Create base frame from first env
        base_frame = self.envs[0].render(mode="rgb_array")
        print(f"Rendering with {self.n_agents}")
        if base_frame is None:
            return None

        # Convert to float32 for easy drawing
        combined_frame = base_frame.astype(np.uint8)

        print(f"Rendering with {self.n_agents}")

        # Overlay other agents
        for i in range(self.n_agents):
            # Get agent's position and angle
            x, y = self.agent_positions[i]
            angle = self.agent_angles[i]
            
            # Convert Box2D coords to pixel coords
            # CarRacing-v3 has 96x96 window by default
            pixel_x = int(np.clip(x, 0, self.width - 1))
            pixel_y = int(np.clip(y, 0, self.height - 1))

            # Draw a simple rectangle or triangle representing the car
            car_size = 5  # pixels
            pts = np.array([
                [pixel_x + car_size, pixel_y],
                [pixel_x - car_size, pixel_y - car_size],
                [pixel_x - car_size, pixel_y + car_size]
            ], np.int32)
            
            # Rotate points around center by angle
            rot_matrix = cv2.getRotationMatrix2D((pixel_x, pixel_y), np.degrees(-angle), 1.0)
            pts = cv2.transform(np.array([pts]), rot_matrix)[0]

            # Draw the polygon
            cv2.fillPoly(combined_frame, [pts.astype(np.int32)], color=(255, 0, 0))
        
        if mode == "human":
            cv2.imshow("Multi-Agent CarRacing", combined_frame)
            cv2.waitKey(int(1000 / self.metadata["render_fps"]))
        elif mode == "rgb_array":
            return combined_frame

    def close(self):
        """Close all environments."""
        for env in self.envs:
            env.close()
    
    def seed(self, seed: Optional[int] = None):
        """Set random seed for reproducibility."""
        for i, env in enumerate(self.envs):
            env.seed(seed + i if seed is not None else None)


class MultiAgentCarRacingWrapper:
    """
    Wrapper for easier integration with MARL algorithms
    """
    
    def __init__(self, n_agents: int = 2, **kwargs):
        self.env = MultiAgentCarRacingEnv(n_agents=n_agents, **kwargs)
        self.n_agents = n_agents
    
    def reset(self, seed=None):
        return self.env.reset(seed=seed)
    
    def step(self, actions):
        return self.env.step(actions)
    
    def render(self):
        print("stuffffff")
        return self.env.render(True, "human")
    
    def close(self):
        return self.env.close()
    
    @property
    def observation_space(self):
        return self.env.observation_space
    
    @property
    def action_space(self):
        return self.env.action_space


# Example usage and testing
# if __name__ == "__main__":
#     # Create multi-agent environment
#     env = MultiAgentCarRacingWrapper(
#         n_agents=2,
#         continuous=True,
#         frame_stack=4,
#         grayscale=True,
#         render_mode="human"
#     )
    
#     print(f"Number of agents: {env.n_agents}")
#     print(f"Observation space: {env.observation_space}")
#     print(f"Action space: {env.action_space}")
    
#     # Test the environment
#     obs, info = env.reset(seed=42)
#     print(f"Initial observations shape: {[o.shape for o in obs]}")
    
#     for step in range(100):
#         # Sample random actions for each agent
#         actions = []
#         for i in range(env.n_agents):
#             if env.env.continuous:
#                 action = np.random.uniform(low=-1.0, high=1.0, size=3)
#             else:
#                 action = env.env.envs[i].action_space.sample()
#             actions.append(action)
        
#         obs, rewards, dones, truncateds, info = env.step(actions)
        
#         print(f"Step {step}: Rewards = {rewards}, Dones = {dones}")
        
#         if all(dones):
#             print("All agents finished!")
#             break
    
#     env.close()