import gymnasium
from gymnasium.wrappers import RecordVideo
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.atari_wrappers import WarpFrame
from stable_baselines3.common.vec_env import VecFrameStack, VecVideoRecorder
from stable_baselines3.common.callbacks import BaseCallback, EvalCallback
from stable_baselines3.common.evaluation import evaluate_policy
from stable_baselines3.common.vec_env import VecTransposeImage
from stable_baselines3.common.callbacks import CallbackList, CheckpointCallback

if __name__ == "__main__":
    gray_scale = True
    # If gray_scale True, convert obs to gray scale 84 x 84 image
    wrapper_class = WarpFrame if gray_scale else None
    # env = gymnasium.make('CarRacing-v3')
    # Create Training environment
    seed = 1
    env = make_vec_env("CarRacing-v3",
        n_envs=1,
        wrapper_class=wrapper_class, 
        seed=1
    )
    env = VecFrameStack(env, n_stack=4)
    env = VecTransposeImage(env)

    # Create Evaluation environment
    env_val = make_vec_env("CarRacing-v3", n_envs=1, wrapper_class=wrapper_class)
    env_val = VecFrameStack(env_val, n_stack=4)
    env_val = VecTransposeImage(env_val)
    
    model = PPO("CnnPolicy", env, verbose=1, ent_coef=0.0075)
    print("Training model...")
    model.learn(total_timesteps=1000000, progress_bar=True)
    model.save("ppo_car_racing")

    mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=20)
    print(f"Final Model - Mean reward: {mean_reward:.2f} +/- {std_reward:.2f}")
    print("Model saved")

