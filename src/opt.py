import cv2
import numpy as np
from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3.common.vec_env import VecTransposeImage, VecFrameStack
from stable_baselines3.common.atari_wrappers import WarpFrame
import copy 
def render_action_direction(env, bad_car_pos, action, arrow_length=50):
    """
    Render the main environment and overlay the "optimal" action direction
    according to the custom action mapping:
        0: do nothing
        1: steer right
        2: steer left
        3: gas
        4: brake
    """
    car_env = env.envs[0].unwrapped
    frame = car_env.render()  # RGB array
    frame = np.ascontiguousarray(frame)

    viewport_w, viewport_h = frame.shape[1], frame.shape[0]

    car_x, car_y = bad_car_pos
    scroll_x = car_x - viewport_w / 2
    scroll_y = car_y - viewport_h / 2

    # Map discrete action to directional vector
    dx, dy = 0, 0
    if action == 1:  # steer right
        dx = arrow_length
    elif action == 2:  # steer left
        dx = -arrow_length
    elif action == 3:  # gas
        dy = -arrow_length  # up
    elif action == 4:  # brake
        dy = arrow_length  # down
    # action 0: do nothing → dx, dy = 0

    start_pt = (int(car_x - scroll_x), int(viewport_h - (car_y - scroll_y)))
    end_pt = (int(start_pt[0] + dx), int(start_pt[1] + dy))

    # Draw arrow for optimal action
    cv2.arrowedLine(frame, start_pt, end_pt, color=(0, 0, 255), thickness=3, tipLength=0.3)

    # Draw bad car position as blue circle
    cv2.circle(frame, start_pt, radius=6, color=(255, 0, 0), thickness=-1)

    cv2.imshow("CarRacing Optimal Action Visualization", frame)
    cv2.waitKey(1)



if __name__ == "__main__":
    seed = 1
    env_kwargs = {"continuous": False, "render_mode": "rgb_array"}

    # Main environment for the bad model
    bad_env = make_vec_env(
        "CarRacing-v3",
        n_envs=1,
        env_kwargs=env_kwargs,
        wrapper_class=WarpFrame,
        seed=seed,
    )
    bad_env = VecFrameStack(bad_env, n_stack=4)
    bad_env = VecTransposeImage(bad_env)

    # Load models
    bad_model = DQN.load("dpo_post_trained", env=bad_env, verbose=0)
    good_model = DQN.load("dpo_post_trained", env=bad_env, verbose=0)

    obs = bad_env.reset()
    deterministic = True

    # copied = copy.deepcopy(bad_env)

    while True:
        # Step bad model
        action, _ = bad_model.predict(obs, deterministic=False)
        obs, rewards, dones, infos = bad_env.step(action)

        # Bad car position
        bad_car_env = bad_env.envs[0].unwrapped
        bad_car_pos = tuple(bad_car_env.car.hull.position)

        # Query the good model for optimal action (no stepping)
        optimal_action, _ = good_model.predict(obs, deterministic=False)

        # Render
        render_action_direction(bad_env, bad_car_pos, optimal_action)

        if dones.any():
            obs = bad_env.reset()
