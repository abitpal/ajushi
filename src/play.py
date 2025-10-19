import numpy as np
import torch
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecFrameStack, VecTransposeImage
from stable_baselines3.common.atari_wrappers import WarpFrame
from marl_env import MultiAgentCarRacingWrapper
from dqn import DQNAgent  # Import DQNAgent from dqn.py
import matplotlib.pyplot as plt
from typing import List, Dict, Any
import time

model_path = "kuds/car-racing-dqn"


class MultiAgentDQNSimulation:
    """
    Multi-Agent DQN Simulation for Car Racing
    
    This class manages multiple DQN agents playing simultaneously
    in the multi-agent car racing environment.
    """
    
    def __init__(
        self, 
        n_agents: int = 2,
        should_train_agents: bool = True,
        model_paths: List[str] = None,
        render_mode: str = "human",
        episode_length: int = 1000
    ):
        self.n_agents = n_agents
        self.should_train_agents = should_train_agents
        self.model_paths = model_paths or [f"dqn_agent_{i}" for i in range(n_agents)]
        self.render_mode = render_mode
        self.episode_length = episode_length
        
        # Initialize agents
        self.agents = []
        self.training_histories = []
        
        # Create MARL environment
        self.marl_env = MultiAgentCarRacingWrapper(
            n_agents=n_agents,
            continuous=False,  # DQN needs discrete actions
            frame_stack=4,
            grayscale=True,
            render_mode=render_mode
        )
        
        # Initialize DQN agents using DQNAgent class
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize DQN agents using DQNAgent class."""
        for i in range(self.n_agents):
            if self.should_train_agents:
                # Create new DQN agent for training
                agent = DQNAgent(
                    agent_id=i,
                    train_new=True,
                    repo_id=model_path,
                    filename="best_model.zip",    
                    marl_env = self.marl_env
                )
                self.agents.append(agent)
            else:
                # Try to load pre-trained agent
                try:
                    agent = DQNAgent(
                        agent_id=i,
                        model_path=self.model_paths[i]
                    )
                    self.agents.append(agent)
                except:
                    print(f"Could not load agent {i}, creating new one")
                    agent = DQNAgent(
                        agent_id=i,
                        train_new=True,
                        repo_id=model_path,
                        filename="best_model.zip",
                        marl_env = self.marl_env
                    )
                    self.agents.append(agent)
    
    def train_agents(self, total_timesteps: int = 50000, save_models: bool = True):
        """Train all DQN agents independently."""
        print(f"Training {self.n_agents} DQN agents for {total_timesteps} timesteps each...")
        
        for i, agent in enumerate(self.agents):
            print(f"\nTraining Agent {i+1}/{self.n_agents}")
            print("-" * 50)
            
            # Train the agent
            agent.learn(total_timesteps=total_timesteps, progress_bar=True)
            
            # Save the model
            if save_models:
                agent.save(self.model_paths[i])
                print(f"Saved agent {i} to {self.model_paths[i]}")
        
        print("\nTraining completed!")
    
    def play_episode(self, deterministic: bool = True, render: bool = True) -> Dict[str, Any]:
        """Play a single episode with all agents."""
        obs, info = self.marl_env.reset()
        
        episode_rewards = [0.0] * self.n_agents
        episode_length = 0
        done = False
        
        print(f"Starting episode with {self.n_agents} agents...")
        
        while not done and episode_length < self.episode_length:
            # Get actions from all agents
            actions = []
            for i, agent in enumerate(self.agents):
                # Convert observation to the format expected by DQN
                agent_obs = self._convert_obs_for_agent(obs[i], agent)
                action, _ = agent.predict(agent_obs, deterministic=deterministic)
                actions.append(action)
            
            # Step the environment
            obs, rewards, dones, truncateds, info = self.marl_env.step(actions)
            
            # Update episode rewards
            for i in range(self.n_agents):
                episode_rewards[i] += rewards[i]
            
            episode_length += 1
            
            # Render if requested
            if render and self.render_mode == "human":
                self.marl_env.render()
                time.sleep(0.02)  # Control rendering speed
            
            # Check if all agents are done
            done = all(dones) or all(truncateds)
        
        results = {
            "episode_rewards": episode_rewards,
            "episode_length": episode_length,
            "agent_dones": dones,
            "agent_truncateds": truncateds
        }
        
        return results
    
    def _convert_obs_for_agent(self, obs: np.ndarray, agent: DQNAgent) -> np.ndarray:
        """Convert MARL observation to DQN agent format."""
        # The observation should already be in the correct format (C, H, W)
        # But we need to ensure it matches what the agent expects
        return obs
    
    def evaluate_agents(self, n_episodes: int = 10) -> Dict[str, Any]:
        """Evaluate all agents over multiple episodes."""
        print(f"Evaluating agents over {n_episodes} episodes...")
        
        all_rewards = [[] for _ in range(self.n_agents)]
        episode_lengths = []
        
        for episode in range(n_episodes):
            print(f"Episode {episode + 1}/{n_episodes}")
            
            results = self.play_episode(deterministic=True, render=False)
            
            for i in range(self.n_agents):
                all_rewards[i].append(results["episode_rewards"][i])
            
            episode_lengths.append(results["episode_length"])
        
        # Calculate statistics
        evaluation_results = {}
        for i in range(self.n_agents):
            rewards = all_rewards[i]
            evaluation_results[f"agent_{i}"] = {
                "mean_reward": np.mean(rewards),
                "std_reward": np.std(rewards),
                "min_reward": np.min(rewards),
                "max_reward": np.max(rewards)
            }
        
        evaluation_results["episode_lengths"] = {
            "mean": np.mean(episode_lengths),
            "std": np.std(episode_lengths)
        }
        
        return evaluation_results
    
    def plot_training_results(self):
        """Plot training results for all agents."""
        if not self.training_histories:
            print("No training history available. Train agents first.")
            return
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle("Multi-Agent DQN Training Results", fontsize=16)
        
        # Plot rewards for each agent
        for i, history in enumerate(self.training_histories):
            axes[0, 0].plot(history["rewards"], label=f"Agent {i}")
        axes[0, 0].set_title("Episode Rewards")
        axes[0, 0].set_xlabel("Episode")
        axes[0, 0].set_ylabel("Reward")
        axes[0, 0].legend()
        axes[0, 0].grid(True)
        
        # Plot episode lengths
        for i, history in enumerate(self.training_histories):
            axes[0, 1].plot(history["episode_lengths"], label=f"Agent {i}")
        axes[0, 1].set_title("Episode Lengths")
        axes[0, 1].set_xlabel("Episode")
        axes[0, 1].set_ylabel("Length")
        axes[0, 1].legend()
        axes[0, 1].grid(True)
        
        # Plot loss (if available)
        for i, history in enumerate(self.training_histories):
            if "loss" in history:
                axes[1, 0].plot(history["loss"], label=f"Agent {i}")
        axes[1, 0].set_title("Training Loss")
        axes[1, 0].set_xlabel("Step")
        axes[1, 0].set_ylabel("Loss")
        axes[1, 0].legend()
        axes[1, 0].grid(True)
        
        # Plot exploration rate
        for i, history in enumerate(self.training_histories):
            if "exploration_rate" in history:
                axes[1, 1].plot(history["exploration_rate"], label=f"Agent {i}")
        axes[1, 1].set_title("Exploration Rate")
        axes[1, 1].set_xlabel("Step")
        axes[1, 1].set_ylabel("Epsilon")
        axes[1, 1].legend()
        axes[1, 1].grid(True)
        
        plt.tight_layout()
        plt.show()
    
    def close(self):
        """Close all environments and clean up."""
        self.marl_env.close()
        for agent in self.agents:
            if hasattr(agent, 'model') and hasattr(agent.model, 'env'):
                agent.model.env.close()


def main():
    """Main function to run the multi-agent DQN simulation."""
    print("Multi-Agent DQN Car Racing Simulation")
    print("=" * 50)
    
    # Create simulation
    simulation = MultiAgentDQNSimulation(
        n_agents=2,
        should_train_agents=False,  # Set to False to load pre-trained models
        render_mode="human",
        episode_length=1000
    )
    
    # Train agents
    # print("\nTraining agents...")
    # simulation.train_agents(total_timesteps=25000, save_models=True)
    
    # Evaluate agents
    print("\nEvaluating agents...")
    eval_results = simulation.evaluate_agents(n_episodes=5)
    
    # Print evaluation results
    print("\nEvaluation Results:")
    print("-" * 30)
    for agent_name, stats in eval_results.items():
        if agent_name.startswith("agent_"):
            print(f"{agent_name}:")
            print(f"  Mean Reward: {stats['mean_reward']:.2f} ± {stats['std_reward']:.2f}")
            print(f"  Min Reward: {stats['min_reward']:.2f}")
            print(f"  Max Reward: {stats['max_reward']:.2f}")
    
    print(f"\nEpisode Length: {eval_results['episode_lengths']['mean']:.1f} ± {eval_results['episode_lengths']['std']:.1f}")
    
    # Play a demonstration episode
    print("\nPlaying demonstration episode...")
    demo_results = simulation.play_episode(deterministic=True, render=True)
    
    print(f"\nDemo Episode Results:")
    for i, reward in enumerate(demo_results["episode_rewards"]):
        print(f"Agent {i}: {reward:.2f}")
    
    # Clean up
    simulation.close()
    print("\nSimulation completed!")


if __name__ == "__main__":
    main()