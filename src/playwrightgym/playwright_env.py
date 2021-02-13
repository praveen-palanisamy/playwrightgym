#!/usr/bin/env python

import gym
import typing
from playwright.sync_api import sync_playwright
from PIL import Image
import io
import numpy as np
import string


# Generate an index mapped character list: ["", a, b, c, ... x, y, z, " "]
KEY_ACTION_MAP = {i: x for (i, x) in enumerate(list("" + string.ascii_uppercase + " "))}


class PlaywrightEnv(gym.Env):
    def __init__(self, env_config: typing.Dict = {}):
        self.env_config = env_config
        self.base_url = env_config.get("url", "http://localhost:8000/login-user.html")
        self.playwright = sync_playwright().start()
        self.obs_im_shape = env_config.get(
            "obs_im_shape", {"width": 160, "height": 260}
        )
        self.obs_im_channels = 3
        self.reward_elem_name = self.env_config.get("reward_elem_name", "reward")
        self.step_num = 0
        self.max_step_num = self.env_config.get("max_step_num", 100)
        self.num_allowed_chars = len(KEY_ACTION_MAP) - 1
        self.observation_space = gym.spaces.Box(
            0,
            255,
            (
                self.obs_im_shape["width"],
                self.obs_im_shape["height"],
                self.obs_im_channels,
            ),
            dtype=int,
        )
        # Action: [x, y, character]
        self.action_space = gym.spaces.Box(
            low=np.array([0, 0, 0]),
            high=np.array(
                [
                    self.obs_im_shape["width"],
                    self.obs_im_shape["height"],
                    self.num_allowed_chars,
                ]
            ),
            shape=(3,),
            dtype=np.float32,  # minval for tf.random.uniform for int is expected to be scalar :?;https://github.com/tensorflow/tensorflow/issues/39814
        )
        self.headless = self.env_config.get("headless", True)
        # self.playwright = sync_playwright()

    def _get_screenshot(self) -> np.ndarray:
        screenshot_bytes = self.page.screenshot()
        screenshot = np.array(Image.open(io.BytesIO(screenshot_bytes)).convert("RGB"))
        return screenshot

    def reset(self) -> np.ndarray:
        self.browser = self.playwright.chromium.launch(headless=self.headless)
        self.page = self.browser.new_page()
        self.page.set_viewport_size(self.obs_im_shape)
        self.page.set_default_navigation_timeout(1000)
        self.page.goto(self.base_url)
        self.obs = self._get_screenshot()
        self.step_num = 0
        self.done = False
        return self.obs

    def step(self, action):
        # action: [click_x, click_y, press_key]
        click_x, click_y, press_key_id = action
        press_key = KEY_ACTION_MAP.get(press_key_id, "")
        if not self.done:
            self.page.mouse.click(float(click_x), float(click_y))
            if not press_key == "":  # Skip key
                self.page.keyboard.press(press_key)
            self.obs = self._get_screenshot()
            self.step_num += 1
            if self.step_num >= self.max_step_num:
                self.done = True
            # Reward is +1 on task completion; -1 otherwise
            # TODO: Is per-step reward useful or reward at episode end enough?
            self.reward = self.page.evaluate("get_reward()") if self.done else -1
            self.info = {}
            return self.obs, self.reward, self.done, self.info
        else:
            raise (ValueError("Episode done. Call reset()"))

    def close(self):
        self.browser.close()
        self.playwright.stop()
        super().close()


if __name__ == "__main__":
    env_config = {}
    env = PlaywrightEnv(env_config=env_config)
    done = False
    obs = env.reset()
    step_num = 0
    while not done:
        action = env.action_space.sample()
        next_obs, reward, done, info = env.step(action)
        print(
            f"Step#:{step_num} obs.shape:{next_obs.shape} Action:{action} Reward:{reward} Done:{done} Info:{info}"
        )
        step_num += 1
        # Debug:
        # Image.fromarray(next_obs).show()
        # input()
    env.close()
