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
    def __init__(self, env_config: typing.Dict):
        self.env_config = env_config
        self.base_url = env_config.get("url", "file://login-user.html")
        self.obs_im_shape = env_config.get(
            "obs_im_shape", {"width": 160, "height": 210}
        )
        self.reward_elem_name = self.env_config.get("reward_elem_name", "reward")
        self.step_num = 0
        self.max_step_num = self.env_config.get("max_step_num", 100)
        self.headless = self.env_config.get("headless", False)
        self.playwright = sync_playwright()
        with self.playwright as p:
            self.browser = p.chromium.launch(headless=self.headless)

    def _get_screenshot(self) -> np.ndarray:
        screenshot_bytes = self.page.screenshot()
        screenshot = np.array(Image.open(io.BytesIO(screenshot_bytes)))
        return screenshot

    def reset(self) -> np.ndarray:
        with self.playwright:
            self.page = self.browser.new_page()
            self.page.set_viewport_size(self.obs_im_shape)
            self.page.goto(self.base_url)
            self.obs = self._get_screenshot()
            self.step_num = 0
            return self.obs

    def step(self, action):
        # action: [click_x, click_y, press_key]
        click_x, click_y, press_key_id = action
        press_key = KEY_ACTION_MAP.get(press_key_id, "")
        with self.playwright:
            if not self.done:
                self.page.mouse.click(click_x, click_y)
                self.page.keyboard.press(press_key)
                self.obs = self._get_screenshot()
                self.reward = self.page.get(self.reward_elem_name, "value")
                self.step_num += 1
                if self.step_num >= self.max_step_num:
                    self.done = True
                self.info = {}
                return self.obs, self.reward, self.done, self.info
            else:
                raise (ValueError("Episode done. Call reset()"))


if __name__ == "__main__":
    env_config = {}
    env = PlaywrightEnv(env_config=env_config)
    done = False
    obs = env.reset()
    while not done:
        action = env.action_space.sample()
        next_obs, reward, done, info = env.step(action)
        print(
            f"obs.shape:{next_obs.shape} \t Reward:{reward} \t Done:{done} \t Info:{info}"
        )
        input()