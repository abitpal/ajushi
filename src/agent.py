from env_setup import CarRacingWrapper
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env

if __name__ == "__main__":
    # env = CarRacingWrapper(continuous=True, frame_stack=4, grayscale=True, render_mode="human")
    env = make_vec_env("CarRacing-v3", n_envs=1)


    # while not done:
    #     action = env.env.action_space.sample()  # Random action
    #     obs, reward, done, info = env.step(action)
    #     total_reward += reward
    #     env.render()


    model = PPO("CnnPolicy", env)
    model.learn(total_timesteps=10000)
    model.save("ppo_car_racing")
    print("Model saved")

    obs = env.reset()
    while True:
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        env.render("human")

    print(f"Episode finished with total reward: {total_reward}")
    env.close()