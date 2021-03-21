#!/usr/bin/env python
# Script to collect human demonstrations in Playwright-Gym environments

from argparse import ArgumentParser

import cv2
import gym
import numpy as np
import playwrightgym

parser = ArgumentParser("playwright-gym_human_player")
parser.add_argument(
    "--env-name",
    default="PlaywrightLoginUserVisualEnv-v0",
    help="playwright-gym Env name. Default=PlaywrightLoginUserVisualEnv-v0",
)
parser.add_argument(
    "--num-episodes", default=2, help="Number of episodes to play. Default=2"
)


class Demonstrator(object):
    def __init__(self, env_name: str):
        self.env_name = env_name
        self.env = gym.make(self.env_name)
        self.window_name = "Playwright-Gym-demo-collector"
        cv2.namedWindow(self.window_name)
        cv2.setMouseCallback(self.window_name, self.mouse_handler)
        self.obs = np.zeros(self.env.observation_space.shape)
        self.action = {"x": 0, "y": 0, "key_idx": 0}
        # Create a key_action_map: {keyboard_char: key_idx}
        self.ord_key_action_map = {
            v: k for k, v in playwright_gym.ACTION_KEY_MAP.items()
        }

    def mouse_handler(self, event, x, y, flags, params):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.action["x"], self.action["y"] = x, y
            cv2.circle(
                self.obs, (x, y), radius=5, color=(0, 255, 0), thickness=cv2.FILLED
            )
            # Refresh the window to show the circle drawn on self.obs
            cv2.imshow(self.window_name, self.obs)

    def get_action(self, obs):
        """Show obs to human, get demo action

        Args:
            obs (env.observation_space): Obs
        """
        self.obs = obs
        cv2.imshow(self.window_name, obs)
        print("Listening for mouse click event & waiting for key input")
        key = cv2.waitKey(0)  # Blocking request for keyboard input
        key_char = chr(key).upper()

        if key_char in self.ord_key_action_map:
            self.action["key_idx"] = self.ord_key_action_map[key_char]
        # else: TODO(praveenp) Handle invalid actions & reset prev action or include NOOP action in env
        return np.array([self.action["x"], self.action["y"], self.action["key_idx"]])


if __name__ == "__main__":
    args = parser.parse_args()
    demonstrator = Demonstrator(args.env_name)
    for ep in range(args.num_episodes):
        done = False
        obs = demonstrator.env.reset()
        step = 0
        while not done:
            action = demonstrator.get_action(obs)
            obs, reward, done, info = demonstrator.env.step(action)
            print(
                f"Ep#:{ep} step#:{step} obs.shape:{obs.shape} rew:{reward} done:{done}"
            )
            step += 1
