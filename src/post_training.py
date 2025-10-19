# from huggingface_hub import hf_hub_download
import torch as th
import numpy as np
import gymnasium as gym
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.vec_env import VecFrameStack
from stable_baselines3.common.atari_wrappers import WarpFrame
import cv2

# Download the model from the Hub
# model_path = hf_hub_download(repo_id="kuds/car-racing-dqn", filename="best_model.zip")

# Create the environment
seed = 1
env_kwargs_dict={"continuous": False}
env = make_vec_env("CarRacing-v3", n_envs=1, env_kwargs=env_kwargs_dict, wrapper_class=WarpFrame, seed=1)
env = VecFrameStack(env, n_stack=4)
env = VecTransposeImage(env)

# Load the model
model_path = "dpo_post_trained.zip"
model = DQN.load(model_path, env=env, verbose=1)

n_steps = 2048
# model.learn(total_timesteps=n_steps * 5, progress_bar=True)

# model.save("dpo_post_trained")

# Enjoy the trained agent
obs = env.reset()
dones = np.zeros(shape=(5,1))

while not dones.all(): 
    action, _states = model.predict(obs, deterministic=True)
    obs, rewards, dones, info = env.step(action)
    # Get car position
    car = env.envs[0].unwrapped.car
    x, y = car.hull.position

    # Convert render to numpy image
    frame = env.render()

    # Draw text or circle on top of frame
    overlay = frame.copy()
    cv2.putText(overlay, f"Pos: ({x:.1f}, {y:.1f})", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    
    # Optional: visualize
    cv2.imshow("Custom Render", overlay)
    if cv2.waitKey(1) == ord('q'):
        break

    # env.render("human")
