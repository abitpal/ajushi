from huggingface_hub import hf_hub_download
import torch as th
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.atari_wrappers import WarpFrame

# Download the model from the Hub
model_path = hf_hub_download(repo_id="kuds/car-racing-dqn", filename="best_model.zip")

# Create the environment
seed = 1
env_kwargs_dict={"continuous": False}
env = make_vec_env("CarRacing-v3", n_envs=1, env_kwargs=env_kwargs_dict, wrapper_class=WarpFrame, seed=1)
env = VecFrameStack(env, n_stack=4)
env = VecTransposeImage(env)

# Load the model
model = DQN.load(model_path, env=env, verbose=1)

model.learn(total_timesteps=2048 * 5, progress_bar=True)

model.save("dpo_post_trained")

# Enjoy the trained agent
obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    env.render("human")
