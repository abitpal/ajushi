from env_setup import CarRacingWrapper
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.env_checker import check_env

if __name__ == "__main__":
    # env = CarRacingWrapper(continuous=True, frame_stack=4, grayscale=True, render_mode="human")
    # env = make_vec_env("CarRacing-v3", n_envs=1)

    env = make_vec_env(
        lambda: CarRacingWrapper(
            continuous=True,
            frame_stack=4,
            grayscale=True,
            render_mode=None
        ),
        n_envs=4
    )
    
    print(f"Vectorized environment created with {env.num_envs} environments")
    print(f"Observation space: {env.observation_space}")
    print(f"Action space: {env.action_space}")
    
    # Check environment compatibility
    print("Checking environment compatibility...")
    check_env(env.envs[0])
    print("Environment is compatible!")

    # model = PPO(
    #     "CnnPolicy",
    #     env,
    #     verbose=1,
    #     learning_rate=3e-4,
    #     n_steps=2048,
    #     batch_size=64,
    #     n_epochs=10,
    #     gamma=0.99,
    #     gae_lambda=0.95,
    #     clip_range=0.2,
    #     ent_coef=0.0,
    #     vf_coef=0.5,
    #     # IMPORTANT: Set normalize_images=False since we're already normalizing
    #     policy_kwargs=dict(
    #         normalize_images=False,  # This is key!
    #         net_arch=[dict(pi=[256, 256], vf=[256, 256])]
    #     )
    # )
    # model.learn(total_timesteps=10000, reset_num_timesteps=False, progress_bar=True)
    # model.save("ppo_rc")
    # print("Model saved")

    # load model
    model = PPO.load("ppo_rc", env=env)
    print("Model loaded")

    print("Testing trained model...")
    test_env = CarRacingWrapper(
        continuous=True,
        frame_stack=4,
        grayscale=True,
        render_mode="human"
    )



    # while not done:
    #     action = env.env.action_space.sample()  # Random action
    #     obs, reward, done, info = env.step(action)
    #     total_reward += reward
    #     env.render()


    # model = PPO("CnnPolicy", env)
    # model.learn(total_timesteps=10000)
    # model.save("ppo_car_racing")
    # print("Model saved")

    # model = PPO.load("ppo_car_racing", env=env)
    # model.learn(total_timesteps=10000, reset_num_timesteps=False, progress_bar=True)
    # model.save("ppo_car_racing")

    obs, info = test_env.reset()
    done = False
    total_reward = 0.0

    while not done:
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, truncated, info = test_env.step(action)
        done = done or truncated
        total_reward += reward
        test_env.render()

    print(f"Episode finished with total reward: {total_reward}")
    test_env.close()
    env.close()