from huggingface_hub import hf_hub_download
import torch as th
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.atari_wrappers import WarpFrame
from typing import Optional

class DQNAgent:
    def __init__(
        self, 
        agent_id: int = 0,
        repo_id: Optional[str] = None, 
        filename: Optional[str] = None,
        train_new: bool = True,
        model_path: Optional[str] = None,
        marl_env=None  # Add MARL environment parameter
    ):
        self.agent_id = agent_id
        self.model = None
        self.env = None  # Store environment reference
        self.marl_env = marl_env  # Store MARL environment reference
        
        if model_path:
            # Load from local path
            self.model = DQN.load(model_path)
            print(f"Loaded DQN agent {agent_id} from {model_path}")
            self._setup_environment()
        elif repo_id and filename:
            # Load from Hugging Face
            try:
                model_path = hf_hub_download(repo_id=repo_id, filename=filename)
                self.model = DQN.load(model_path)
                print(f"Loaded DQN agent {agent_id} from Hugging Face")
                self._setup_environment()
            except Exception as e:
                print(f"Failed to load from Hugging Face: {e}")
                if train_new:
                    self._create_new_model()
                else:
                    raise
        elif train_new:
            # Create new model for training
            self._create_new_model()
        else:
            raise ValueError("Must provide either model_path, repo_id+filename, or set train_new=True")
    
    def _setup_environment(self):
        """Set up environment for loaded models."""
        if self.marl_env is not None:
            # Create individual environment for this agent (for training)
            env_kwargs = {"continuous": False}
            self.env = make_vec_env(
                "CarRacing-v3", 
                n_envs=1, 
                env_kwargs=env_kwargs, 
                wrapper_class=WarpFrame
            )
            self.env = VecFrameStack(self.env, n_stack=4)
            self.env = VecTransposeImage(self.env)
            
            # Set the environment for the model
            if self.model is not None:
                self.model.set_env(self.env)
                self.model.tensorboard_log = None
        else:
            # Create individual environment for this agent
            env_kwargs = {"continuous": False}
            self.env = make_vec_env(
                "CarRacing-v3", 
                n_envs=1, 
                env_kwargs=env_kwargs, 
                wrapper_class=WarpFrame
            )
            self.env = VecFrameStack(self.env, n_stack=4)
            self.env = VecTransposeImage(self.env)
            
            if self.model is not None:
                self.model.set_env(self.env)
    
    def _create_new_model(self):
        """Create a new DQN model for training."""
        print(f"Creating new DQN model for agent {self.agent_id}")
        
        # Create environment for this agent
        env_kwargs = {"continuous": False}
        self.env = make_vec_env(
            "CarRacing-v3", 
            n_envs=1, 
            env_kwargs=env_kwargs, 
            wrapper_class=WarpFrame
        )
        self.env = VecFrameStack(self.env, n_stack=4)
        self.env = VecTransposeImage(self.env)
        
        # Create DQN model
        self.model = DQN(
            "CnnPolicy",
            self.env,  # Pass the environment to the model
            verbose=1,
            learning_rate=1e-4,
            buffer_size=50000,
            learning_starts=10000,
            batch_size=32,
            tau=1.0,
            gamma=0.99,
            train_freq=4,
            gradient_steps=1,
            target_update_interval=1000,
            exploration_fraction=0.1,
            exploration_initial_eps=1.0,
            exploration_final_eps=0.05,
            max_grad_norm=10,
        )
    
    def predict(self, obs, deterministic=True):
        """Make a prediction using the model."""
        if self.model is None:
            raise ValueError("Model not initialized")
        return self.model.predict(obs, deterministic=deterministic)
    
    def learn(self, total_timesteps, progress_bar=True):
        """Train the model."""
        if self.model is None:
            raise ValueError("Model not initialized")
        
        # Ensure environment is set
        if self.model.env is None and self.env is not None:
            self.model.set_env(self.env)
        elif self.model.env is None:
            raise ValueError("Model environment not set. Cannot train without environment.")
            
        return self.model.learn(total_timesteps=total_timesteps, progress_bar=progress_bar)
    
    def save(self, path):
        """Save the model."""
        if self.model is None:
            raise ValueError("Model not initialized")
        self.model.save(path)
        print(f"Saved DQN agent {self.agent_id} to {path}")
    
    def load(self, path):
        """Load a model."""
        self.model = DQN.load(path)
        print(f"Loaded DQN agent {self.agent_id} from {path}")
    
    def set_env(self, env):
        """Set the environment for the model (useful when loading pre-trained models)."""
        if self.model is not None:
            self.model.set_env(env)
            self.env = env
        else:
            raise ValueError("Model not initialized")
    
    def close(self):
        """Close the environment."""
        if self.env is not None:
            self.env.close()