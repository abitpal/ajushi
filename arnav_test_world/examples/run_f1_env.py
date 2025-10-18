import gymnasium as gym
import f1_gymnasium  # noqa: F401 - needed to ensure env registration via import


def main() -> None:
    env = gym.make(
        "f1_gymnasium/F1Strategy-v0",
        render_mode="ansi",
        total_laps=10,
        seed=42,
    )
    obs, info = env.reset()
    done = False
    total_reward = 0.0
    step_count = 0

    while True:
        action = env.action_space.sample()
        obs, reward, terminated, truncated, info = env.step(action)
        total_reward += reward
        step_count += 1

        line = env.render()
        if line:
            print(line)

        if terminated or truncated:
            break

    print(f"Steps: {step_count}, total reward (negative total time): {total_reward:.2f}")


if __name__ == "__main__":
    main()


